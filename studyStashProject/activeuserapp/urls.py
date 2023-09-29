from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('docs/', views.docs, name='docs'),
    path('help/', views.help, name='help'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings, name='settings'),
    path('today_task/', views.today_task, name='today_task'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('active_index/', views.active_index, name='active_index'),
]
