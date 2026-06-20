from django.core.management.base import BaseCommand

from catalog.models import Book
from catalog.utils import normalize_media_url


class Command(BaseCommand):
    help = 'Kitoblardagi noto\'g\'ri PDF va muqova havolalarini tuzatadi'

    def handle(self, *args, **options):
        fixed = 0
        for book in Book.objects.all():
            changed = False
            if book.pdf_url:
                cleaned = normalize_media_url(book.pdf_url)
                if book.pdf_file and '/media/' in cleaned:
                    cleaned = ''
                if cleaned != book.pdf_url:
                    book.pdf_url = cleaned
                    changed = True
            if book.cover_url:
                cleaned = normalize_media_url(book.cover_url)
                if book.cover and '/media/' in cleaned:
                    cleaned = ''
                if cleaned != book.cover_url:
                    book.cover_url = cleaned
                    changed = True
            if changed:
                book.save(update_fields=['pdf_url', 'cover_url'])
                fixed += 1
                self.stdout.write(f'  Tuzatildi: {book.title}')

        self.stdout.write(self.style.SUCCESS(f'{fixed} ta kitob yangilandi.'))
