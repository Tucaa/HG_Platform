from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    #RIVER BASIN
    path('river-basins/', views.RiverBasinList.as_view()),
    path('river-basin/<str:pk>/', views.SingleRiverBasin.as_view()),
    path('create-river-basin/', views.CreateRiverBasin.as_view()),
    # LOCATION
    path('locations/', views.LocationList.as_view()),
    path('location/<str:pk>/', views.SingleLocation.as_view()),
    path('create-location/', views.CreateLocation.as_view()),
    # DATA FOR LOCATION
    path('location/<str:pk>/files/', views.FileList.as_view()),
    path('file/<str:pk>/', views.SingleFile.as_view()),
    path('upload-file/', views.UploadFile.as_view()),
    
]