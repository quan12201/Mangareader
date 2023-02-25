from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.shortcuts import render


# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=224, null=False, blank=False)
    content = models.TextField(max_length=1000, null=False, blank=False)
    type = models.TextField(max_length=224, null=False, blank=False)
    num_of_volumes = models.IntegerField(default=0, null=False, blank=False)
    author = models.TextField(max_length=254, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to='cover')

    def __unicode__(self):
        return self.content
  
    def get_absolute_url(self):
        return reverse('mangas:list-mangas', kwargs={})


def path_file_name(instance, filename):
    result = 'content/' + instance.manga.name + '/' + instance.name + '/' + filename
    return result


def path_chapter_name(instance, filename):
    result = 'content/' + instance.manga.name + '/' + instance.volume.name + '/' + instance.name + '/' + filename
    return result


class Volume(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    # images = models.FileField(upload_to=path_file_name)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, null=True, blank=True)
    num_of_chapters = models.IntegerField(default=0, null=False, blank=False)
    timestamp = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.content 

class Subscription(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=False, blank=False)
    timestamp = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.content    
    

class Chapter(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    images = models.FileField(upload_to=path_chapter_name)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, null=True, blank=True)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self):
        return self.content    

    # def get_absolute_url(self):
    #     return reverse(template_name='mangas/content.html', kwargs={})