from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('kitob/<slug:slug>/', views.book_detail, name='book_detail'),
    path('kitob/<slug:slug>/pdf/', views.book_pdf, name='book_pdf'),
    path('kitob/<slug:slug>/muqova/', views.book_cover, name='book_cover'),
    path('kategoriya/<slug:slug>/', views.category_books, name='category'),
    path('mualliflar/', views.author_list, name='author_list'),
    path('muallif/<slug:slug>/', views.author_detail, name='author_detail'),
]
