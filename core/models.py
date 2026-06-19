from django.db import models
from django.urls import reverse


class Service(models.Model):
    ICON_CHOICES = [
        ('book', 'Kitob'),
        ('badge', 'Medal / sifat'),
        ('people', 'Odamlar'),
        ('truck', 'Yetkazib berish'),
        ('support', 'Qo\'llab-quvvatlash'),
        ('lock', 'Xavfsizlik'),
        ('print', 'Bosma'),
    ]

    title = models.CharField(
        'Xizmat nomi',
        max_length=200,
        help_text='Masalan: Sifatli nashrlar',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda. Masalan: sifatli-nashrlar',
    )
    short_description = models.CharField(
        'Qisqa tavsif',
        max_length=300,
        help_text='Bosh sahifa kartochkasida ko\'rinadigan qisqa matn',
    )
    description = models.TextField(
        'To\'liq tavsif',
        help_text='Xizmatlar sahifasidagi batafsil matn',
    )
    icon = models.CharField(
        'Ikonka',
        max_length=50,
        choices=ICON_CHOICES,
        default='book',
        help_text='Bosh sahifada ko\'rinadigan ikonka turi',
    )
    order = models.PositiveIntegerField(
        'Tartib raqami',
        default=0,
        help_text='Kichik raqam yuqorida ko\'rinadi',
    )
    is_active = models.BooleanField(
        'Faol',
        default=True,
        help_text='O\'chirilsa bosh sahifada ko\'rinmaydi',
    )

    class Meta:
        verbose_name = 'Xizmat'
        verbose_name_plural = 'Xizmatlar (bosh sahifa)'
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:service_detail', kwargs={'slug': self.slug})


class HomeStatistic(models.Model):
    ICON_CHOICES = [
        ('book', 'Kitob'),
        ('people', 'Odamlar'),
        ('medal', 'Medal'),
        ('monitor', 'Monitor / onlayn'),
        ('globe', 'Globus'),
    ]

    icon = models.CharField(
        'Ikonka',
        max_length=50,
        choices=ICON_CHOICES,
        default='book',
        help_text='Statistika kartochkasidagi ikonka',
    )
    value = models.CharField(
        'Qiymat',
        max_length=100,
        help_text='Masalan: 2000+, 10+, Bepul',
    )
    label = models.CharField(
        'Sarlavha',
        max_length=200,
        help_text='Masalan: Nashr etilgan kitoblar',
    )
    description = models.TextField(
        'Tavsif',
        help_text='Kartochka ostidagi qisqa izoh',
    )
    order = models.PositiveIntegerField(
        'Tartib raqami',
        default=0,
        help_text='Kichik raqam chapdan boshlab ko\'rinadi',
    )
    is_active = models.BooleanField(
        'Faol',
        default=True,
        help_text='O\'chirilsa bosh sahifada ko\'rinmaydi',
    )

    class Meta:
        verbose_name = 'Bosh sahifa statistikasi'
        verbose_name_plural = 'Bosh sahifa statistikasi'
        ordering = ['order']

    def __str__(self):
        return f'{self.value} — {self.label}'


class ContactMessage(models.Model):
    name = models.CharField('Ism', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Telefon', max_length=20, blank=True)
    subject = models.CharField('Mavzu', max_length=200, blank=True)
    message = models.TextField('Xabar')
    created_at = models.DateTimeField('Yuborilgan sana', auto_now_add=True)

    class Meta:
        verbose_name = 'Aloqa xabari'
        verbose_name_plural = 'Aloqa xabarlari'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject or "Xabar"}'


class NewsletterSubscriber(models.Model):
    email = models.EmailField('Email', unique=True)
    created_at = models.DateTimeField('Obuna sanasi', auto_now_add=True)

    class Meta:
        verbose_name = 'Obunachi'
        verbose_name_plural = 'Obunachilar'

    def __str__(self):
        return self.email
