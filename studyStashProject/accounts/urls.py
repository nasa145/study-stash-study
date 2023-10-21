
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('success_register/', views.success_register_view, name='success_register'),
    # path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('profile/', views.profile, name='profile'),
    path('available_plans/', views.available_plans_view, name='available_plans'),
    path('not-found/', views.not_found_view, name='not_found'),

    # URLS FOR PASSWORD RESET WHICH IS CUSTOM
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('password_reset/done/', views.custom_password_reset_done, name='password_reset_done'),
    path('password_reset/confirm/<str:uidb64>/<str:token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/complete/', views.custom_password_reset_complete, name='password_reset_complete'),

    # a password change that is custom
    path('password_change/', views.password_change, name='password_change'),
]