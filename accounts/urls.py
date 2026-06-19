from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('kirish/', views.login_view, name='login'),
    path('royxat/', views.register_view, name='register'),
    path('chiqish/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
]
