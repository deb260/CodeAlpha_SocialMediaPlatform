from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('explore/', views.explore, name='explore'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('settings/profile/', views.edit_profile, name='edit_profile'),
]
