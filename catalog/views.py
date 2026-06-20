from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Sum
import mimetypes

from .models import Book, BookCategory, Author
from .utils import normalize_media_url


def get_book_categories():
    return BookCategory.objects.filter(is_active=True).order_by('order', 'name')


def book_list(request):
    books = Book.objects.select_related('author', 'category')
    category_slug = request.GET.get('kategoriya')
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'newest')
    lang = request.GET.get('til', '')
    file_format = request.GET.get('format', '')

    if category_slug:
        books = books.filter(category__slug=category_slug)
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    if lang:
        books = books.filter(language=lang)
    if file_format:
        books = books.filter(file_format__iexact=file_format)

    sort_map = {'newest': '-created_at', 'title': 'title', 'year': '-year', 'popular': '-download_count'}
    books = books.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(books, 12)
    page = paginator.get_page(request.GET.get('page'))

    total_downloads = Book.objects.aggregate(total=Sum('download_count'))['total'] or 0

    context = {
        'books': page,
        'books_count': books.count(),
        'categories': get_book_categories(),
        'active_category': category_slug,
        'query': query,
        'sort': sort,
        'lang': lang,
        'file_format': file_format,
        'total_books': Book.objects.count(),
        'total_authors': Author.objects.count(),
        'total_downloads': total_downloads,
    }
    return render(request, 'catalog/book_list.html', context)


def book_detail(request, slug):
    book = get_object_or_404(Book.objects.select_related('author', 'category'), slug=slug)
    Book.objects.filter(pk=book.pk).update(views=book.views + 1)
    book.views += 1
    related = Book.objects.filter(category=book.category).exclude(pk=book.pk)[:6]
    other_books = Book.objects.exclude(pk=book.pk).order_by('-download_count')[:5]
    return render(request, 'catalog/book_detail.html', {
        'book': book,
        'book_share_url': book.get_share_url(request),
        'related_books': related,
        'other_books': other_books,
        'categories': get_book_categories(),
        'active_category': book.category.slug,
        'total_books': Book.objects.count(),
    })


def book_pdf(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if book.pdf_file:
        try:
            content_type = mimetypes.guess_type(book.pdf_file.name)[0] or 'application/pdf'
            response = FileResponse(
                book.pdf_file.open('rb'),
                content_type=content_type,
                filename=f'{book.slug}.pdf',
            )
            if request.GET.get('download'):
                response['Content-Disposition'] = f'attachment; filename="{book.slug}.pdf"'
            return response
        except FileNotFoundError:
            pass
    if book.pdf_url:
        target = normalize_media_url(book.pdf_url)
        if target.startswith('/'):
            return redirect(target)
        return redirect(book.pdf_url)
    raise Http404('PDF mavjud emas')


def book_cover(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if not book.cover:
        raise Http404('Muqova topilmadi')
    try:
        content_type = mimetypes.guess_type(book.cover.name)[0] or 'image/jpeg'
        return FileResponse(book.cover.open('rb'), content_type=content_type)
    except FileNotFoundError:
        raise Http404('Muqova fayli topilmadi')


def category_books(request, slug):
    category = get_object_or_404(BookCategory, slug=slug, is_active=True)
    books = Book.objects.filter(category=category).select_related('author')
    return render(request, 'catalog/category.html', {'category': category, 'books': books})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'catalog/author_list.html', {'authors': authors})


def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    books = author.books.select_related('category').all()
    return render(request, 'catalog/author_detail.html', {'author': author, 'books': books})
