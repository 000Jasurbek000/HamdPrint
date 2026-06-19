from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('maqolalar/', views.article_list, name='article_list'),
    path('maqola/<slug:slug>/', views.article_detail, name='article_detail'),
    path('', views.news_list, name='list'),
    path('<slug:slug>/', views.news_detail, name='detail'),
]
