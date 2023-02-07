from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

from . import views


router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')

app_name = 'news'
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('tag/<slug:tag_slug>', views.TagView.as_view(), name='tag'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('signin', views.SigninView.as_view(), name='signin'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('signout', LogoutView.as_view(), name='signout'),
]
