from django.urls import path
from . import views

app_name='studystashapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('legal/', views.legal_information, name='legal_information'),
]
