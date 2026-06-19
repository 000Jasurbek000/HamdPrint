from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum

from catalog.models import Book
from .models import NewsPost, Article, NewsCategory, ArticleCategory


def get_news_categories():
    return NewsCategory.objects.filter(is_active=True).order_by('order', 'name')


def get_article_categories():
    return ArticleCategory.objects.filter(is_active=True).order_by('order', 'name')


def news_list(request):
    news = NewsPost.objects.filter(is_published=True).select_related('category')
    category_slug = request.GET.get('kategoriya', '')
    sort = request.GET.get('sort', 'newest')

    if category_slug:
        news = news.filter(category__slug=category_slug)
    if sort == 'popular':
        news = news.order_by('-views')
    else:
        news = news.order_by('-published_at')

    paginator = Paginator(news, 5)
    page = paginator.get_page(request.GET.get('page'))

    published_news = NewsPost.objects.filter(is_published=True)
    context = {
        'news_list': page,
        'latest_news': published_news.select_related('category')[:5],
        'news_categories': get_news_categories(),
        'active_category': category_slug,
        'sort': sort,
        'total_news': published_news.count(),
        'total_news_views': published_news.aggregate(total=Sum('views'))['total'] or 0,
        'total_news_categories': get_news_categories().count(),
    }
    return render(request, 'blog/news_list.html', context)


def news_detail(request, slug):
    post = get_object_or_404(NewsPost.objects.select_related('category'), slug=slug, is_published=True)
    NewsPost.objects.filter(pk=post.pk).update(views=post.views + 1)
    post.views += 1
    prev_post = NewsPost.objects.filter(is_published=True, published_at__lt=post.published_at).order_by('-published_at').first()
    next_post = NewsPost.objects.filter(is_published=True, published_at__gt=post.published_at).order_by('published_at').first()
    return render(request, 'blog/news_detail.html', {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'latest_news': NewsPost.objects.filter(is_published=True).exclude(pk=post.pk).order_by('-published_at')[:5],
        'latest_books': Book.objects.order_by('-created_at')[:5],
    })


def article_list(request):
    articles_qs = Article.objects.filter(is_published=True).select_related('category')
    category_slug = request.GET.get('kategoriya', '')
    sort = request.GET.get('sort', '')

    if category_slug:
        articles_qs = articles_qs.filter(category__slug=category_slug)
    if sort in ('popular', 'views'):
        articles_qs = articles_qs.order_by('-views')
    else:
        articles_qs = articles_qs.order_by('-published_at')

    paginator = Paginator(articles_qs, 8)
    page = paginator.get_page(request.GET.get('page'))

    published_articles = Article.objects.filter(is_published=True)
    category_items = [
        {
            'slug': cat.slug,
            'label': cat.name,
            'count': published_articles.filter(category=cat).count(),
        }
        for cat in get_article_categories()
    ]
    context = {
        'articles': page,
        'category_items': category_items,
        'total_articles': published_articles.count(),
        'total_article_views': published_articles.aggregate(total=Sum('views'))['total'] or 0,
        'total_article_authors': published_articles.values('author_name').distinct().count(),
        'active_category': category_slug,
        'sort': sort,
    }
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article.objects.select_related('category'), slug=slug, is_published=True)
    Article.objects.filter(pk=article.pk).update(views=article.views + 1)
    article.views += 1
    prev_art = Article.objects.filter(is_published=True, published_at__lt=article.published_at).order_by('-published_at').first()
    next_art = Article.objects.filter(is_published=True, published_at__gt=article.published_at).order_by('published_at').first()
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'prev_art': prev_art,
        'next_art': next_art,
        'latest_articles': Article.objects.filter(is_published=True).exclude(pk=article.pk).order_by('-published_at')[:5],
        'latest_books': Book.objects.order_by('-created_at')[:5],
    })
