from django import forms
from .models import Manga, Volume, Chapter

class CreateMangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = ['name', 'content', 'type', 'cover']

class CreateVolumeForm(forms.ModelForm):
    class Meta:
        model = Volume
        fields = ['name', 'manga']
        widgets = {
            'images': forms.FileInput(attrs={'multiple': True})
        }

class CreateChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['volume', 'name', 'images', 'manga']
        widgets = {
            'images': forms.FileInput(attrs={'multiple': True})
        }
        