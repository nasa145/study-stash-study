from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('password_reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
    path('password_reset/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password_reset/form/', views.password_reset_form_view, name='password_reset_form'),
    path('phone_verification/', views.phone_verification_view, name='phone_verification'),
    path('register/', views.register_view, name='register'),
    path('success_register/', views.success_register_view, name='success_register'),
    path('available-plans/', views.available_plans_view, name='available_plans'),
    path('not-found/', views.not_found_view, name='not_found'),
]
