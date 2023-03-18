from django.urls import path
from . import views

app_name = 'public_def'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_request, name='api_request'),
    path('authorize/', views.authorize, name='authorize'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    # path('google_login/', views.google_login, name='google_login'),
    # path('google_login/callback', views.google_login_callback,
    #      name='google_login_callback'),
    path('result/', views.result, name='result'),
]
