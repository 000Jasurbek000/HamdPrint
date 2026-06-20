import os
import re
from urllib.parse import unquote, urlparse


def book_cover_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower() or '.jpg'
    return f'books/covers/{instance.slug}{ext}'


def book_pdf_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower() or '.pdf'
    return f'books/pdf/{instance.slug}{ext}'


def normalize_media_url(url):
    """Havolani tozalash — takrorlangan /media/ yo'llarini tuzatadi."""
    if not url:
        return ''
    url = unquote(url.strip())
    if url.startswith(('http://', 'https://')):
        return url

    parsed = urlparse(url)
    if parsed.scheme:
        url = parsed.path

    url = re.sub(r'/+', '/', url)
    if 'media/books/pdf/' in url:
        url = '/media/books/pdf/' + url.split('media/books/pdf/')[-1]
    elif 'media/books/covers/' in url:
        url = '/media/books/covers/' + url.split('media/books/covers/')[-1]
    elif not url.startswith('/'):
        url = '/' + url
    return url
