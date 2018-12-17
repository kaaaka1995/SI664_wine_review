from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('wines/', views.WineListView.as_view(), name='wines'),
    path('wines/<int:pk>/', views.WineDetailView.as_view(), name='wine_detail'),
]