from django.urls import path
from . import views

app_name = 'habit'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_pixel/', views.add_pixel, name='add_pixel'),
    path('delete_pixel/', views.delete_pixel, name='delete_pixel'),
    path('create_graph/', views.create_graph, name='create_graph'),
    path('delete_graph/', views.delete_graph, name='delete_graph'),
]
