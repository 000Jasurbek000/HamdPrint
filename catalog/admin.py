from django.contrib import admin
from .models import BookCategory, Author, Book


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'book_count_display']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    fieldsets = (
        (None, {
            'description': (
                'Kitob kategoriyasini yarating. Avval kategoriya qo\'shing, '
                'keyin kitoblarni shu kategoriyaga biriktiring.'
            ),
            'fields': ('name', 'slug', 'description'),
        }),
        ('Ko\'rinish', {
            'fields': ('order', 'is_active'),
        }),
    )

    @admin.display(description='Kitoblar soni')
    def book_count_display(self, obj):
        return obj.book_count


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'books_count']
    search_fields = ['name', 'bio']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'description': 'Kitob muallifini qo\'shing. Slug avtomatik yaratiladi.',
            'fields': ('name', 'slug', 'bio', 'photo_url'),
        }),
    )

    @admin.display(description='Kitoblar')
    def books_count(self, obj):
        return obj.books.count()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'year', 'is_featured', 'views']
    list_filter = ['category', 'is_featured', 'year', 'language']
    search_fields = ['title', 'author__name', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured']
    autocomplete_fields = ['author', 'category']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Asosiy', {
            'description': 'Kitobning asosiy ma\'lumotlari. Muallif va kategoriya oldindan yaratilgan bo\'lishi kerak.',
            'fields': ('title', 'slug', 'author', 'category', 'cover_url', 'description'),
        }),
        ('Nashr ma\'lumotlari', {
            'fields': ('publisher', 'year', 'pages', 'language', 'file_format', 'file_size'),
        }),
        ('Fayllar', {
            'description': 'PDF yoki onlayn o\'qish havolalarini kiriting.',
            'fields': ('pdf_url', 'read_online_url'),
        }),
        ('Qo\'shimcha', {
            'classes': ('collapse',),
            'fields': ('table_of_contents', 'about_points', 'download_count', 'views', 'is_featured'),
        }),
    )
