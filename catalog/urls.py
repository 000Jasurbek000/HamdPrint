from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),
    path('book/<slug:slug>/pdf/', views.book_pdf, name='book_pdf'),
    path('book/<slug:slug>/cover/', views.book_cover, name='book_cover'),
    path('category/<slug:slug>/', views.category_books, name='category'),
    path('authors/', views.author_list, name='author_list'),
    path('author/<slug:slug>/', views.author_detail, name='author_detail'),
]
