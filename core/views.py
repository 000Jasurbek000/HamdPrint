from datetime import datetime, date

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from catalog.models import Book, BookCategory, Author
from blog.models import NewsPost, NewsCategory
from .models import ContactMessage, NewsletterSubscriber, Service
from .home_page import get_home_categories_with_counts


def home(request):
    if request.method == 'POST' and request.POST.get('form') == 'home_contact':
        ContactMessage.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, 'Xabaringiz muvaffaqiyatli yuborildi!')
        return redirect('core:home')

    return render(request, 'core/home.html', {
        'home_categories': get_home_categories_with_counts(),
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, 'Xabaringiz muvaffaqiyatli yuborildi!')
        return redirect('core:contact')
    return render(request, 'core/contact.html')


def services(request):
    context = {'services': Service.objects.filter(is_active=True)}
    return render(request, 'core/services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'core/service_detail.html', {'service': service})


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'Yangiliklarga muvaffaqiyatli obuna bo\'ldingiz!')
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))


def _sort_key(value):
    if value is None:
        return 0.0
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime.combine(value, datetime.min.time()).timestamp()
    if isinstance(value, datetime):
        return value.timestamp()
    return 0.0


def _build_search_results(books_qs, news_qs, tab):
    results = []
    if tab in ('all', 'books'):
        for book in books_qs:
            results.append({
                'type': 'kitob',
                'type_label': 'Kitob',
                'title': book.title,
                'excerpt': book.description[:200] if book.description else '',
                'image': book.cover_src,
                'url': book.get_absolute_url(),
                'date': book.created_at,
                'views': book.views,
                'author': book.author.name,
                'category': book.category.name,
                'sort_date': book.created_at,
            })
    if tab in ('all', 'news'):
        for post in news_qs:
            results.append({
                'type': 'yangilik',
                'type_label': 'Yangilik',
                'title': post.title,
                'excerpt': post.excerpt,
                'image': post.image_url,
                'url': post.get_absolute_url(),
                'date': post.published_at,
                'views': post.views,
                'author': 'BUKHARA HAMD PRINT',
                'category': post.category_display,
                'sort_date': post.published_at,
            })
    results.sort(key=lambda x: _sort_key(x['sort_date']), reverse=True)
    return results


def search(request):
    query = request.GET.get('q', '').strip()
    tab = request.GET.get('tab', 'all')
    cat_slug = request.GET.get('kategoriya', '')
    author_slug = request.GET.get('muallif', '')
    year_from = request.GET.get('yildan', '')
    year_to = request.GET.get('yilgacha', '')
    fmt = request.GET.get('format', '')

    if fmt == 'kitob':
        tab = 'books'
    elif fmt == 'yangilik':
        tab = 'news'

    books_qs = Book.objects.select_related('author', 'category')
    news_qs = NewsPost.objects.filter(is_published=True).select_related('category')

    if query:
        books_qs = books_qs.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query) | Q(description__icontains=query)
        )
        news_qs = news_qs.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query)
        )

    if cat_slug:
        books_qs = books_qs.filter(category__slug=cat_slug)
        news_qs = news_qs.filter(category__slug=cat_slug)

    if author_slug:
        books_qs = books_qs.filter(author__slug=author_slug)

    if year_from and year_from.isdigit():
        books_qs = books_qs.filter(year__gte=int(year_from))
        news_qs = news_qs.filter(published_at__year__gte=int(year_from))
    if year_to and year_to.isdigit():
        books_qs = books_qs.filter(year__lte=int(year_to))
        news_qs = news_qs.filter(published_at__year__lte=int(year_to))

    books_count = books_qs.count()
    news_count = news_qs.count()
    total_count = books_count + news_count

    results = _build_search_results(books_qs, news_qs, tab)
    paginator = Paginator(results, 8)
    page = paginator.get_page(request.GET.get('page'))

    categories = BookCategory.objects.filter(is_active=True)
    category_counts = {}
    base_books = Book.objects.all()
    if query:
        base_books = base_books.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query) | Q(description__icontains=query)
        )
    for cat in categories:
        category_counts[cat.slug] = base_books.filter(category=cat).count()

    categories_with_counts = [(cat, category_counts.get(cat.slug, 0)) for cat in categories]

    params = {'q': query}
    if tab != 'all':
        params['tab'] = tab
    if cat_slug:
        params['kategoriya'] = cat_slug
    if author_slug:
        params['muallif'] = author_slug
    if year_from:
        params['yildan'] = year_from
    if year_to:
        params['yilgacha'] = year_to
    if fmt:
        params['format'] = fmt

    if tab == 'books':
        visible_count = books_count
    elif tab == 'news':
        visible_count = news_count
    else:
        visible_count = total_count

    context = {
        'query': query,
        'tab': tab,
        'results': page,
        'total_count': total_count,
        'visible_count': visible_count,
        'filter_params': params,
        'books_count': books_count,
        'news_count': news_count,
        'categories_with_counts': categories_with_counts,
        'categories': categories,
        'authors': Author.objects.all(),
        'active_category': cat_slug,
        'active_author': author_slug,
        'year_from': year_from,
        'year_to': year_to,
        'active_format': fmt,
    }
    return render(request, 'core/search.html', context)


def robots_txt(request):
    content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /account/
Disallow: /subscribe/
"""
    return HttpResponse(content, content_type='text/plain')
