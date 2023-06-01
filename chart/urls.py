from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'chart'

urlpatterns = [
    path('', views.index, name='index'),
    path('hayul_growth/', login_required(views.ChartView.as_view(),
         login_url='common:login'), name='growth_chart'),
    path('hayul_growth/get_data/', views.get_data, name='growth_data'),
    path('hayul_growth/list/', login_required(views.HayulGrowthListView.as_view(),
         login_url='common:login'), name='growth_list'),
    path('hayul_growth/add/', login_required(views.HayulGrowthCreateView.as_view(),
         login_url='common:login'), name='growth_add'),
    path('hayul_growth/<int:pk>/',
         login_required(views.HayulGrowthUpdateView.as_view(),
                        login_url='common:login'), name='growth_update'),
    path('hayul_growth/<int:pk>/delete',
         login_required(views.HayulGrowthDeleteView.as_view(),
                        login_url='common:login'), name='growth_delete'),
]
