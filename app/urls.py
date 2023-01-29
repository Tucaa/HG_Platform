from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    #Register url
    path('register/', views.registerPage, name="register"),
    path('', views.home, name='home'),
    path('location/<str:pk>/', views.location, name="location"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('create-location/', views.createLocation, name="create-location"),
    path('update-location/<str:pk>/', views.updateLocation, name="update-location"),
    path('delete-location/<str:pk>/', views.deleteLocation, name="delete-location"),
    path('delete-file/<str:pk>/', views.deleteFile, name="delete-file"),
    path('update-user/', views.updateUser, name="update-user"),
    path('basins/', views.basinsPage, name="basins"),
    path('activity/', views.activityPage, name="activity"),
    path('location/data-view/<str:pk>/', views.dataView, name="data-view"),
    #Upload form
    path('location/<str:pk>/upload-file/', views.uploadFile, name="upload-file"),
]