from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateMangaForm, CreateVolumeForm, CreateChapterForm
from django.urls import reverse
from zipfile import ZipFile
from notifications.signals import notify

from django.contrib.auth.models import User
from .models import Manga, Chapter, Subscription, Volume

# Create your views here.
class ListMangaView(ListView):
    model = Manga
    def get(self, request, *args, **kwargs):
        template_name = 'mangas/list-mangas.html'
        notifications = ''
        if request.user.username == '':
            print("anonymous")
        else:
            user = User.objects.get(username=request.user.username)
            # print(user.notifications.unread())
            notifications = user.notifications.unread()
            print(len(notifications))

            for notification in user.notifications.unread():
                print(notification.verb)
            print(request.user.username)
            
        obj = {
            'mangas': Manga.objects.all(),
            'username': request.user.username,
            'notifications': notifications,
            'num_of_notifications': len(notifications),
            # 'user': User.objects.get(id=1)
            # 'notifications'
            # 'len': len(request.user.username),
        }
        # print("a",request.user.username, "aa")
        return render(request, template_name, obj)


class CreateMangaView(SuccessMessageMixin, CreateView):
    template_name = 'mangas/create-manga.html'
    form_class = CreateMangaForm
    success_message = 'Create Manga successfully!'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            author = request.user.username
            cover = request.FILES.get('cover')
            data = request.POST
            Manga.objects.create(name=data['name'], content=data['content'], type=data['type'], author=author, cover=cover)
            return redirect('mangas:list-mangas')
        else:
            print("invalid")
            return self.form_invalid(form)
        

def search_mangas(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        mangas = Manga.objects.filter(name__icontains=keyword)
        template_name = 'mangas/search_mangas.html'

        print(mangas)

        notifications = ''
        if request.user.username == '':
            print("anonymous")
        else:
            user = User.objects.get(username=request.user.username)
            # print(user.notifications.unread())
            notifications = user.notifications.unread()
            print(len(notifications))

            for notification in user.notifications.unread():
                print(notification.verb)
            print(request.user.username)
            
        obj = {
            'mangas': mangas,
            'username': request.user.username,
            'notifications': notifications,
            'num_of_notifications': len(notifications),
            'searched': keyword,
        }

        return render(request, template_name, obj)
    else:
        template_name = 'mangas/search_mangas.html'
        obj = {
        }
        return render(request, template_name, obj)


class UpdateMangaView(SuccessMessageMixin, UpdateView):
    template_name = 'mangas/edit-manga.html'
    model = Manga
    fields = ['name', 'content', 'type']
    success_message = 'Update Manga successfully!'

    def get_success_url(self): 
        return reverse('mangas:list-mangas', kwargs={})
    

class ListVolumeView(ListView):
    model = Volume
    def get(self, request, pk, *args, **kwargs):
        template_name = 'mangas/list-volumes.html'
        username = request.user.username
        manga = Manga.objects.get(id=pk)
        volumes = Volume.objects.values('name', 'manga_id', 'timestamp').distinct()
        # volumes = Volume.objects.filter(manga=manga)
        lst = []
        for i in range(len(volumes)):
            if volumes[i]['manga_id'] == pk:
                lst.append(volumes[i])

        volumes = lst
        print(volumes)

        for i in range(len(volumes)):
            # print(volume.id)
            volume = Volume.objects.get(name=volumes[i]['name'], manga=manga)
            chapter = Chapter.objects.filter(volume=volume)[0]
            # print(chapters)
            lst[i]['chapter'] = chapter.name

        
        # for i in range(len(volumes)):
        #     volume = Volume.objects.filter(name=volumes[i]['name'], manga=manga)
        #     chapter = Chapter.objects.filter(volume=volume)
        #     print(chapter)
        #     volumes[i]['chapter'] = chapter.name 
        
        print(len(volumes))

        is_subscribed = 2
        if Subscription.objects.filter(manga_id=pk, username=username).exists() == True:
            is_subscribed = 1
        else:
            is_subscribed = 0
        # print(is_subscribed)
        obj = {
            'volumes': volumes,
            'username': username,
            'manga': Manga.objects.get(id=pk),
            'is_subscribed': is_subscribed,
        }
        return render(request, template_name, obj)


# class DisplayContentView(ListView):
#     model = Volume
#     def get(self, request, pk, volume_id, *args, **kwargs):
#         template_name = 'mangas/content.html'
#         volumes = Volume.objects.filter(name=volume_id)
#         obj = {
#             'volumes': Chapter.objects.filter(volume=volumes[0]),
#             'manga': Manga.objects.get(id=pk)
#         }
#         return render(request, template_name, obj)
    

class DisplayContentView(ListView):
    model = Chapter
    def get(self, request, pk, volume_id, chapter_name, *args, **kwargs):
        template_name = 'mangas/content.html'
        manga = Manga.objects.get(id=pk)
        volume = Volume.objects.get(name=volume_id, manga=manga)
        chapters = Chapter.objects.filter(volume=volume, name=chapter_name, manga=manga)
        all_chapters = Chapter.objects.filter(manga=manga)
        chapter_names = all_chapters.values('name', 'volume_id', 'manga_id').distinct()
        lst = []
        cur_chapter = chapters.values('name', 'volume_id', 'manga_id').distinct()[0]

        for name in chapter_names:
            lst.append(name)

        prev_chapter = ''
        next_chapter = ''
        next_volume = ''
        prev_volume = ''
        next = 'chapter'
        prev = 'chapter'    
    
        # print(lst)
        cur = lst.index(cur_chapter)
        if cur < len(lst) - 1:
            next_chapter = lst[cur + 1]['name']
            next_volume = Volume.objects.get(id=lst[cur + 1]['volume_id'])
        if cur > 0:
            prev_chapter = lst[cur - 1]['name']
            prev_volume = Volume.objects.get(id=lst[cur - 1]['volume_id'])
        
        # print(next_volume, prev_volume)

        if next_volume != '' and next_volume.name != volume.name:
            next = 'volume'
        if prev_volume != '' and prev_volume.name != volume.name: 
            prev = 'volume'
        obj = {
            'volume': volume,
            'chapters': chapters,
            'chapterName': cur_chapter['name'],
            'manga': manga,
            'next_chapter': next_chapter,
            'prev_chapter': prev_chapter,
            'next_vol': next_volume,
            'prev_vol': prev_volume,
            'prev': prev,
            'next': next,
        }
        return render(request, template_name, obj)



class MyMangasView(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'mangas/my-mangas.html'


        mangas = Manga.objects.filter(author=request.user.username)
        obj = {
            'mangas': mangas,
        }
        return render(request, template_name, obj)
    

class UploadVolumeView(SuccessMessageMixin, CreateView):
    model = Volume
    template_name = 'mangas/upload-volume.html'
    form_class = CreateVolumeForm
    success_url = 'mangas:list-mangas'


    def post(self, request, pk, *args, **kwargs):
        manga = Manga.objects.get(id=pk)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        sender = User.objects.get(username=request.user.username)
        receivers = Subscription.objects.filter(manga_id=pk)
        for receiver_user in receivers:
            receiver = User.objects.get(username=receiver_user.username)
            notify.send(sender=sender, recipient=receiver, verb=pk, description='New volume from ' + manga.name)

        images = request.FILES.getlist('images')
        for image in images:
            print(image.name)
        data = request.POST
        num_of_chapters = data['num_of_chapters']
        num_of_pages = 0
        volume_name = data['name']
        cur_page = 1
        cur_chap = 1
        new_volumes = 1
        if num_of_chapters != 'Each file is a chapter':
            num_of_chapters = int(num_of_chapters)
            num_of_pages = int(len(images) / num_of_chapters)
        else:
            num_of_chapters = len(images)

        if volume_name == '' and images[0].name[-4:] != '.zip':
            volume_name = 'Volume ' + str(manga.num_of_volumes + 1)
        
        if images[0].name[-4:] != '.zip':
            volume = Volume.objects.create(name=volume_name, manga=manga, num_of_chapters=num_of_chapters)
        
        if form.is_valid():
            print("valid")
            # print(images)
            for image in images:
                if image.name[-4:] != '.zip':
                    if data['num_of_chapters'] == 'Each file is a chapter':
                        print('default')
                        Chapter.objects.create(name = 'Chapter ' + str(cur_chap), images = image, manga=manga, volume=volume)
                        cur_chap += 1
                    else:
                        # print(type(num_of_volumes))
                        print('Cur page:', cur_page, 'Cur chap:', cur_chap)
                        Chapter.objects.create(name='Chapter ' + str(cur_chap), images=image, manga=manga, volume=volume)
                        cur_page += 1
                        if cur_page > num_of_pages and cur_chap < num_of_chapters:
                            cur_page = 1
                            cur_chap += 1

                    
                else:
                    print("zip files")
                    # Chapter.objects.create(images=image, name=data['name'], manga=manga)
                    with ZipFile(image, "r") as zf:
                        print(volume_name)
                        if data['name'] == '':
                            volume_name = image.name[:-4]
                        extract_path = 'media/content/' + manga.name + '/' + volume_name
                        print(extract_path)
                        zf.extractall(path=extract_path)

                        chapters = []
                        for img in zf.namelist():
                            chapter = img.split('/')[0]
                            if chapter not in chapters:
                                chapters.append(chapter)
                        
                        if data['num_of_chapters'] == 'Each file is a chapter':
                            num_of_chapters = len(chapters)
                            volume = Volume.objects.create(name=volume_name, manga=manga, num_of_chapters=num_of_chapters)
                            for img_name in zf.namelist():
                                chapter = img_name.split('/')[0]
                                img = 'content/' + manga.name + '/' + volume_name + '/' + img_name
                                Chapter.objects.create(name=chapter, images=img, manga=manga, volume=volume)
                        else:
                            volume = Volume.objects.create(name=volume_name, manga=manga, num_of_chapters=num_of_chapters)
                            cur_page = 1
                            cur_chap = 1
                            num_of_pages = int(len(zf.namelist()) / num_of_chapters)
                            print(num_of_chapters, num_of_pages)
                            for img_name in zf.namelist():
                                img = 'content/' + manga.name + '/' + volume_name + '/' + img_name
                                print('Cur page:', cur_page, 'Cur chap:', cur_chap)
                                Chapter.objects.create(name='Chapter ' + str(cur_chap), images=img, manga=manga, volume=volume)
                                cur_page += 1
                                if cur_page > num_of_pages and cur_chap < num_of_chapters:
                                    cur_page = 1
                                    cur_chap += 1
                    new_volumes = len(images)
            
            manga.num_of_volumes += new_volumes    
            manga.save()
            return redirect('mangas:list-mangas')
        else:
            print("invalid")
            return self.form_invalid(form)

    def get_success_url(self): 
        return reverse('mangas:list-mangas', kwargs={})
    


class UploadChapterView(SuccessMessageMixin, CreateView):
    model = Volume
    template_name = 'mangas/upload-chapter.html'
    form_class = CreateChapterForm

    def get(self, request, pk, *args, **kwargs):
        template_name = 'mangas/upload-chapter.html'
        manga = Manga.objects.get(id=pk)
        lst = Volume.objects.filter(manga=manga)
        volumes = lst
        # print(lst[0])
        # for i in range(len(lst)):
        #     if i == 0 or lst[i]['name'] != lst[i - 1]['name']:
        #         volumes.add(lst[i])
        print(volumes) 
        

        obj = {
            'volumes': volumes
        }
        return render(request, template_name, obj)
    
    def post(self, request, pk, *args, **kwargs):
        manga = Manga.objects.get(id=pk)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        sender = User.objects.get(username=request.user.username)
        receivers = Subscription.objects.filter(manga_id=pk)
        

        images = request.FILES.getlist('images')
        for image in images:
            print(image.name)
        data = request.POST
        print(data['volume'])
        volumes = Volume.objects.filter(name=data['volume'], manga=manga)
        vol = volumes[0]
        print(vol.name)
        # print('Name: ', data['name'])

        for receiver_user in receivers:
            receiver = User.objects.get(username=receiver_user.username)
            notify.send(sender=sender, recipient=receiver, verb=pk, description='New update of ' + vol.name + ' from ' + manga.name)

        for image in images:
            # print(type(image))
            if image.name[-4:] != '.zip':
                print("image files")
                if data['name'] == '':
                    lst = Chapter.objects.filter(volume=vol)
                    chapters = lst.values('name').distinct()
                    print(chapters)
                    Chapter.objects.create(images=image, name='Chapter ' + str(len(chapters) + 1), manga=manga, volume=vol)
                else:
                    Chapter.objects.create(images=image, name= data['name'], manga=manga, volume=vol)
            else:
                print("zip files")
                # Chapter.objects.create(images=image, name=data['name'], manga=manga)
                with ZipFile(image, "r") as zf:
                    # extract_path = 'media/content/' + manga.name + '/' + vol.name + '/' + data['name']
                    # print(extract_path)
                    # zf.extractall(path=extract_path)
                    if data['name'] == '':
                        chapter_name = image.name[:-4]
                        extract_path = 'media/content/' + manga.name + '/' + vol.name + '/' + chapter_name
                        print(extract_path)
                        zf.extractall(path=extract_path)
                        for img_name in zf.namelist():
                            # chapter_name = image.name[:-4]
                            img = 'content/' + manga.name + '/' + vol.name + '/' + chapter_name + '/' + img_name
                            print(img_name, '||', img)
                            print()
                            Chapter.objects.create(images=img, name=chapter_name, manga=manga, volume=vol)
                    else:
                        for img_name in zf.namelist():
                            extract_path = 'media/content/' + manga.name + '/' + vol.name + '/' + data['name']
                            print(extract_path)
                            zf.extractall(path=extract_path)
                            img = 'content/' + manga.name + '/' + vol.name + '/' + data['name'] + '/' + img_name
                            print(img)
                            Chapter.objects.create(images=img, name=data['name'], manga=manga, volume=vol)

        return redirect('mangas:list-mangas')
    
        

        # if form.is_valid():
        #     print("valid")
        #     return redirect('mangas:list-mangas')
        # else:
        #     print("invalid")
        #     return self.form_invalid(form)
    
    def get_success_url(self): 
        return reverse('mangas:list-mangas', kwargs={})


def read_notifications(request):
    user = User.objects.get(username=request.user.username)
    # notifications = user.notifications.unread()
    request.user.notifications.mark_all_as_read()
    notifications = user.notifications.unread()
    
    obj = {
        'mangas': Manga.objects.all(),
        'username': request.user.username,
        'notifications': notifications,
        'num_of_notifications': len(notifications),
    }

    return render(request, 'mangas/list-mangas.html', obj)



def delete_manga(request, pk):
    manga = Manga.objects.get(id=pk)
    chapters = Chapter.objects.filter(manga_id=manga.id)
    volumes = Volume.objects.filter(manga_id=manga.id)
    subscription = Subscription.objects.filter(manga_id=manga.id)
    manga.delete()
    chapters.delete()
    subscription.delete()
    volumes.delete()
    context = {
        'messages': ['Delete Manga successfully'],
        'mangas': Manga.objects.all(),
    }
    return render(request, 'mangas/list-mangas.html', context)


def subscribe_manga(request, pk):
    manga = Manga.objects.get(id=pk)
    Subscription.objects.create(manga=manga, username=request.user.username)
    context = {
        'message': ['Subscribe Manga successfully'],
        'mangas': Manga.objects.all(),
    }
    success_message = 'Subscribe Manga successfully'

    return render(request, 'mangas/list-mangas.html', context)
    # return reverse('mangas:list-mangas', kwargs={})

