from django.contrib import admin
from .models import NewsCategory, ArticleCategory, NewsPost, Article


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'news_count_display']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'description': (
                'Yangilik kategoriyasini yarating (masalan: Yangi nashrlar, Tadbirlar). '
                'Keyin yangiliklarni shu kategoriyaga biriktiring.'
            ),
            'fields': ('name', 'slug', 'description', 'order', 'is_active'),
        }),
    )

    @admin.display(description='Yangiliklar')
    def news_count_display(self, obj):
        return obj.news_count


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'article_count_display']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'description': (
                'Maqola kategoriyasini yarating (masalan: Din, Ilm-fan). '
                'Keyin maqolalarni shu kategoriyaga biriktiring.'
            ),
            'fields': ('name', 'slug', 'description', 'order', 'is_active'),
        }),
    )

    @admin.display(description='Maqolalar')
    def article_count_display(self, obj):
        return obj.article_count


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published_at', 'views', 'is_published']
    list_filter = ['is_published', 'category', 'published_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    autocomplete_fields = ['category']
    date_hierarchy = 'published_at'

    fieldsets = (
        ('Asosiy', {
            'description': 'Yangilik matnini kiriting. Kategoriya oldindan yaratilgan bo\'lishi kerak.',
            'fields': ('title', 'slug', 'category', 'image_url', 'excerpt', 'content'),
        }),
        ('Nashr', {
            'fields': ('published_at', 'reading_time', 'is_published', 'views'),
        }),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author_name', 'published_at', 'views', 'is_published']
    list_filter = ['is_published', 'category', 'published_at']
    search_fields = ['title', 'excerpt', 'content', 'author_name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    autocomplete_fields = ['category']
    date_hierarchy = 'published_at'

    fieldsets = (
        ('Asosiy', {
            'description': 'Maqola matnini kiriting. Kategoriya oldindan yaratilgan bo\'lishi kerak.',
            'fields': ('title', 'slug', 'category', 'author_name', 'image_url', 'excerpt', 'content'),
        }),
        ('Fayl', {
            'fields': ('pdf_url',),
        }),
        ('Nashr', {
            'fields': ('published_at', 'reading_time', 'is_published', 'views'),
        }),
    )
