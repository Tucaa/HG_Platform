from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('locations/', views.getLocations),
    path('locations/<str:pk>/', views.getLocation),
    
]