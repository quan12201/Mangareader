from django.urls import path
from django.contrib import admin
from mangas.views import (
  ListMangaView,
  CreateMangaView,
  UpdateMangaView,
  UploadVolumeView,
  UploadChapterView,
  DisplayContentView,
  ListVolumeView,
  MyMangasView,
)
from mangas import views

app_name = 'mangas'

urlpatterns = [
    path('list-mangas/', ListMangaView.as_view(), name='list-mangas'),
    path('create-manga/', CreateMangaView.as_view(), name='create-manga'),
    path('my-mangas/', MyMangasView.as_view(), name='my-mangas'),
    path('update-manga/<int:pk>', UpdateMangaView.as_view(), name='update-manga'),
    path('delete-manga/<int:pk>', views.delete_manga, name='delete-manga'),
    path('upload-volume/<int:pk>', UploadVolumeView.as_view(), name='upload-volume'),
    path('upload-chapter/<int:pk>', UploadChapterView.as_view(), name='upload-chapter'),
    path('display-volume/<int:pk>', ListVolumeView.as_view(), name='display-volume'),
    path('content/<int:pk>/<str:volume_id>/<str:chapter_name>', DisplayContentView.as_view(), name='content'),
    path('subscribe-manga/<int:pk>', views.subscribe_manga, name='subscribe-manga'),
    path('search_results/', views.search_mangas, name='search'),
    path('read-notiifcations/', views.read_notifications, name='read-notifications')
]