from django.urls import path
from . import views

app_name='paymentapp'

urlpatterns = [
    path('available_plans/', views.available_plans_view, name='available_plans'),

    path('process/<int:id>/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
