from django.urls import path

from . import views


app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('tag/<slug:tag_slug>', views.TagView.as_view(), name='tag'),
]