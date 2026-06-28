from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from catalog.models import Author, Book, BookCategory
from blog.models import NewsPost
from core.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:contact',
            'core:services',
            'core:search',
            'catalog:book_list',
            'catalog:author_list',
            'blog:list',
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)


class BookSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class BookCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BookCategory.objects.filter(is_active=True)


class AuthorSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Author.objects.all()


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return NewsPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at
