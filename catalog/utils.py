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
        parsed = urlparse(url)
        url = parsed.path or url

    while 'media/books/pdf/' in url[1:]:
        url = '/media/books/pdf/' + url.split('media/books/pdf/')[-1]
    while 'media/books/covers/' in url[1:]:
        url = '/media/books/covers/' + url.split('media/books/covers/')[-1]

    url = re.sub(r'/+', '/', url)
    if not url.startswith('/'):
        url = '/' + url
    return url
