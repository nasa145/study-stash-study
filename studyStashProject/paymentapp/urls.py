from django.urls import path
from . import views

urlpatterns = [
    path('payment_details/', views.payment_details_view, name='payment_details'),
    path('available_plans/', views.available_plans_view, name='available_plans'),
]
