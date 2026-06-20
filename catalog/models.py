from django.db import models
from django.urls import reverse

from .utils import book_cover_upload_path, book_pdf_upload_path, normalize_media_url


class BookCategory(models.Model):
    name = models.CharField(
        'Kategoriya nomi',
        max_length=100,
        help_text='Masalan: Monografiyalar, Darsliklar',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda, bo\'sh joysiz. Masalan: monografiyalar',
    )
    description = models.TextField(
        'Tavsif',
        blank=True,
        help_text='Bosh sahifa va kategoriya kartochkasida ko\'rinadigan qisqa matn',
    )
    order = models.PositiveSmallIntegerField(
        'Tartib raqami',
        default=0,
        help_text='Kichik raqam yuqorida ko\'rinadi (0, 1, 2...)',
    )
    is_active = models.BooleanField(
        'Faol',
        default=True,
        help_text='O\'chirilsa saytda ko\'rinmaydi',
    )

    class Meta:
        verbose_name = 'Kitob kategoriyasi'
        verbose_name_plural = 'Kitob kategoriyalari'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def book_count(self):
        return self.books.count()

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})


class Author(models.Model):
    name = models.CharField(
        'Muallif ismi',
        max_length=200,
        help_text='Kitob muallifining to\'liq ismi',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda. Masalan: abdulloh-qodiriy',
    )
    bio = models.TextField(
        'Biografiya',
        blank=True,
        help_text='Muallif haqida qisqa ma\'lumot (ixtiyoriy)',
    )
    photo_url = models.URLField(
        'Rasm havolasi',
        blank=True,
        help_text='Muallif rasmi URL manzili (ixtiyoriy)',
    )

    class Meta:
        verbose_name = 'Muallif'
        verbose_name_plural = 'Mualliflar'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:author_detail', kwargs={'slug': self.slug})


class Book(models.Model):
    title = models.CharField(
        'Kitob nomi',
        max_length=300,
        help_text='Kitobning to\'liq sarlavhasi',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda, noyob bo\'lishi kerak',
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Muallif',
        help_text='Avval admin paneldan muallif qo\'shing',
    )
    category = models.ForeignKey(
        BookCategory,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Kategoriya',
        help_text='Kitob qaysi kategoriyaga tegishli',
    )
    cover_url = models.URLField(
        'Muqova havolasi',
        blank=True,
        help_text='Muqova rasmi uchun tashqi URL (ixtiyoriy)',
    )
    cover = models.ImageField(
        'Muqova fayli',
        upload_to=book_cover_upload_path,
        blank=True,
        help_text='Kompyuterdan muqova rasmini yuklang (ixtiyoriy)',
    )
    description = models.TextField(
        'Tavsif',
        blank=True,
        help_text='Kitob haqida to\'liq matn',
    )
    publisher = models.CharField(
        'Nashriyot',
        max_length=200,
        default='BUKHARA HAMD PRINT',
        help_text='Nashriyot nomi',
    )
    year = models.PositiveIntegerField(
        'Nashr yili',
        default=2024,
        help_text='Masalan: 2024',
    )
    pages = models.PositiveIntegerField(
        'Sahifalar soni',
        default=0,
        help_text='Kitob sahifalari soni',
    )
    file_format = models.CharField(
        'Fayl formati',
        max_length=20,
        default='PDF',
        help_text='Masalan: PDF, EPUB',
    )
    file_size = models.CharField(
        'Fayl hajmi',
        max_length=50,
        blank=True,
        help_text='Masalan: 4.2 MB',
    )
    pdf_url = models.URLField(
        'PDF havola',
        blank=True,
        help_text='PDF uchun tashqi URL havola (ixtiyoriy)',
    )
    pdf_file = models.FileField(
        'PDF fayl',
        upload_to=book_pdf_upload_path,
        blank=True,
        help_text='Kompyuterdan PDF fayl yuklang (ixtiyoriy)',
    )
    table_of_contents = models.TextField(
        'Mundarija',
        blank=True,
        help_text='Har bir bob yangi qatorda yoziladi',
    )
    language = models.CharField(
        'Til',
        max_length=50,
        default="O'zbekcha",
        help_text='Masalan: O\'zbekcha, Ruscha',
    )
    download_count = models.PositiveIntegerField(
        'Yuklab olishlar',
        default=0,
        help_text='Statistika uchun (avtomatik oshirilishi mumkin)',
    )
    about_points = models.TextField(
        'Kitob haqida punktlar',
        blank=True,
        help_text='Har bir punkt yangi qatorda',
    )
    views = models.PositiveIntegerField(
        'Ko\'rishlar',
        default=0,
        help_text='Sahifa ochilishlari soni',
    )
    is_featured = models.BooleanField(
        'Tanlangan kitob',
        default=False,
        help_text='Bosh sahifada yoki maxsus ro\'yxatda ko\'rsatish uchun',
    )
    created_at = models.DateTimeField('Yaratilgan sana', auto_now_add=True)

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.pdf_url:
            self.pdf_url = normalize_media_url(self.pdf_url)
            if self.pdf_file and '/media/' in self.pdf_url:
                self.pdf_url = ''
        if self.cover_url:
            self.cover_url = normalize_media_url(self.cover_url)
            if self.cover and '/media/' in self.cover_url:
                self.cover_url = ''
        super().save(*args, **kwargs)

    def get_share_url(self, request):
        return request.build_absolute_uri(self.get_absolute_url())

    @property
    def cover_src(self):
        if self.cover:
            return reverse('catalog:book_cover', kwargs={'slug': self.slug})
        return self.cover_url or ''

    @property
    def pdf_link(self):
        if self.has_pdf:
            return reverse('catalog:book_pdf', kwargs={'slug': self.slug})
        return ''

    @property
    def pdf_src(self):
        return self.pdf_link

    @property
    def has_pdf(self):
        return bool(self.pdf_file or self.pdf_url)

    @property
    def has_cover(self):
        return bool(self.cover or self.cover_url)

    @property
    def chapters(self):
        if not self.table_of_contents:
            return []
        return [line.strip() for line in self.table_of_contents.splitlines() if line.strip()]

    @property
    def about_list(self):
        if not self.about_points:
            return self.chapters
        return [line.strip() for line in self.about_points.splitlines() if line.strip()]

    @property
    def read_url(self):
        return self.pdf_src or self.get_absolute_url()
