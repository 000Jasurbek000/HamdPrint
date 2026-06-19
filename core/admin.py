from django.contrib import admin
from .models import Service, HomeStatistic, ContactMessage, NewsletterSubscriber


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'icon']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'description': 'Bosh sahifadagi "Bizning xizmatlarimiz" bo\'limi uchun xizmat qo\'shing.',
            'fields': ('title', 'slug', 'short_description', 'description', 'icon', 'order', 'is_active'),
        }),
    )


@admin.register(HomeStatistic)
class HomeStatisticAdmin(admin.ModelAdmin):
    list_display = ['value', 'label', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'icon']
    search_fields = ['label', 'value', 'description']

    fieldsets = (
        (None, {
            'description': 'Bosh sahifadagi "Raqamlar ortidagi ishonch" statistika kartochkasi.',
            'fields': ('icon', 'value', 'label', 'description', 'order', 'is_active'),
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']

    fieldsets = (
        (None, {
            'description': 'Sayt orqali yuborilgan xabarlar. Faqat ko\'rish mumkin.',
            'fields': readonly_fields,
        }),
    )

    def has_add_permission(self, request):
        return False


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']
    readonly_fields = ['email', 'created_at']

    def has_add_permission(self, request):
        return False
