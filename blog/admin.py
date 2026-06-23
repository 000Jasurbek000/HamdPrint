from django.contrib import admin
from .models import NewsCategory, NewsPost


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
