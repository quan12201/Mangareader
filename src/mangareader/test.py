from mangas.models import Chapter

print(Chapter.objects.values('name'))