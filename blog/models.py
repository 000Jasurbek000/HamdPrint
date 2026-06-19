from django.db import models
from django.urls import reverse


class NewsCategory(models.Model):
    name = models.CharField(
        'Kategoriya nomi',
        max_length=100,
        help_text='Masalan: Yangi nashrlar, Tadbirlar, E\'lonlar',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda. Masalan: yangi-nashrlar',
    )
    description = models.TextField(
        'Tavsif',
        blank=True,
        help_text='Kategoriya haqida qisqa izoh (ixtiyoriy)',
    )
    order = models.PositiveSmallIntegerField(
        'Tartib raqami',
        default=0,
        help_text='Kichik raqam yuqorida ko\'rinadi',
    )
    is_active = models.BooleanField(
        'Faol',
        default=True,
        help_text='O\'chirilsa filtr va ro\'yxatda ko\'rinmaydi',
    )

    class Meta:
        verbose_name = 'Yangilik kategoriyasi'
        verbose_name_plural = 'Yangilik kategoriyalari'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def news_count(self):
        return self.news_posts.filter(is_published=True).count()


class ArticleCategory(models.Model):
    name = models.CharField(
        'Kategoriya nomi',
        max_length=100,
        help_text='Masalan: Din, Ilm-fan, Tarbiya',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda. Masalan: din',
    )
    description = models.TextField(
        'Tavsif',
        blank=True,
        help_text='Kategoriya haqida qisqa izoh (ixtiyoriy)',
    )
    order = models.PositiveSmallIntegerField(
        'Tartib raqami',
        default=0,
        help_text='Kichik raqam yuqorida ko\'rinadi',
    )
    is_active = models.BooleanField(
        'Faol',
        default=True,
        help_text='O\'chirilsa filtr va ro\'yxatda ko\'rinmaydi',
    )

    class Meta:
        verbose_name = 'Maqola kategoriyasi'
        verbose_name_plural = 'Maqola kategoriyalari'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def article_count(self):
        return self.articles.filter(is_published=True).count()


class NewsPost(models.Model):
    title = models.CharField(
        'Sarlavha',
        max_length=300,
        help_text='Yangilik sarlavhasi',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda, noyob bo\'lishi kerak',
    )
    excerpt = models.TextField(
        'Qisqa matn',
        help_text='Ro\'yxat sahifasida ko\'rinadigan qisqa xulosa',
    )
    content = models.TextField(
        'To\'liq matn',
        help_text='Yangilikning to\'liq matni (HTML yoki oddiy matn)',
    )
    image_url = models.URLField(
        'Rasm havolasi',
        help_text='Yangilik asosiy rasmi URL manzili',
    )
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.PROTECT,
        related_name='news_posts',
        verbose_name='Kategoriya',
        help_text='Avval yangilik kategoriyasini tanlang yoki yarating',
    )
    published_at = models.DateField(
        'Nashr sanasi',
        help_text='Yangilik e\'lon qilingan sana',
    )
    views = models.PositiveIntegerField(
        'Ko\'rishlar',
        default=0,
        help_text='Sahifa ochilishlari soni',
    )
    reading_time = models.PositiveIntegerField(
        'O\'qish vaqti (daqiqa)',
        default=5,
        help_text='Taxminiy o\'qish vaqti daqiqalarda',
    )
    is_published = models.BooleanField(
        'Nashr etilgan',
        default=True,
        help_text='O\'chirilsa saytda ko\'rinmaydi',
    )
    created_at = models.DateTimeField('Yaratilgan sana', auto_now_add=True)

    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    @property
    def category_display(self):
        return self.category.name if self.category_id else ''


class Article(models.Model):
    title = models.CharField(
        'Sarlavha',
        max_length=300,
        help_text='Maqola sarlavhasi',
    )
    slug = models.SlugField(
        'Slug (URL)',
        unique=True,
        help_text='Lotin harflarda, noyob bo\'lishi kerak',
    )
    excerpt = models.TextField(
        'Qisqa matn',
        help_text='Ro\'yxat sahifasida ko\'rinadigan qisqa xulosa',
    )
    content = models.TextField(
        'To\'liq matn',
        help_text='Maqolaning to\'liq matni',
    )
    image_url = models.URLField(
        'Rasm havolasi',
        help_text='Maqola asosiy rasmi URL manzili',
    )
    pdf_url = models.URLField(
        'PDF havola',
        blank=True,
        help_text='To\'liq o\'qish uchun PDF havolasi (ixtiyoriy)',
    )
    author_name = models.CharField(
        'Muallif',
        max_length=200,
        default='BUKHARA HAMD PRINT',
        help_text='Maqola muallifi yoki manba',
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.PROTECT,
        related_name='articles',
        verbose_name='Kategoriya',
        help_text='Avval maqola kategoriyasini tanlang yoki yarating',
    )
    published_at = models.DateField(
        'Nashr sanasi',
        help_text='Maqola e\'lon qilingan sana',
    )
    views = models.PositiveIntegerField(
        'Ko\'rishlar',
        default=0,
        help_text='Sahifa ochilishlari soni',
    )
    reading_time = models.PositiveIntegerField(
        'O\'qish vaqti (daqiqa)',
        default=8,
        help_text='Taxminiy o\'qish vaqti daqiqalarda',
    )
    is_published = models.BooleanField(
        'Nashr etilgan',
        default=True,
        help_text='O\'chirilsa saytda ko\'rinmaydi',
    )
    created_at = models.DateTimeField('Yaratilgan sana', auto_now_add=True)

    class Meta:
        verbose_name = 'Maqola'
        verbose_name_plural = 'Maqolalar'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    @property
    def category_display(self):
        return self.category.name if self.category_id else ''

    @property
    def views_display(self):
        if self.views >= 1000:
            val = self.views / 1000
            text = f'{val:.1f}'.rstrip('0').rstrip('.')
            return f'{text}K'
        return str(self.views)
