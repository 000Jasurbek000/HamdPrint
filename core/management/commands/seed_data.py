from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ma\'lumotlarni admin panel orqali qo\'shing (/admin/)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'Bosh sahifa matnlari shablonda doimiy. '
            'Kitoblar, yangiliklar va maqolalarni admin paneldan qo\'shing.'
        ))
