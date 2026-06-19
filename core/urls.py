from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('biz-haqimizda/', views.about, name='about'),
    path('aloqa/', views.contact, name='contact'),
    path('xizmatlar/', views.services, name='services'),
    path('xizmatlar/<slug:slug>/', views.service_detail, name='service_detail'),
    path('qidiruv/', views.search, name='search'),
    path('obuna/', views.newsletter_subscribe, name='newsletter'),
]
