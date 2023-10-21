from django.urls import path
from . import views

app_name='activeuserapp'

urlpatterns = [
    path('account/', views.account, name='account'),
    path('docs/', views.docs, name='docs'),
    path('help/', views.help, name='help'),
    path('notifications/', views.notifications, name='notifications'),
    path('today_task/', views.today_task, name='today_task'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('active_index/', views.active_index, name='active_index'),
    path('legal/', views.legal_information, name='legal_information'),

    # custom urls that will need to be editted
    path('tasks', views.available_tasks, name='tasks'),
    path('download/<int:task_id>/', views.download_task, name='download_task'),

]
