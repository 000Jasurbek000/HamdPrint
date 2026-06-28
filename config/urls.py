from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import robots_txt

admin.site.site_header = 'BUKHARA HAMD PRINT — Admin panel'
admin.site.site_title = 'HAMD PRINT Admin'
admin.site.index_title = 'Kitoblar va yangiliklarni boshqaring'

urlpatterns = [
    path('robots.txt', robots_txt, name='robots_txt'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('books/', include('catalog.urls')),
    path('news/', include('blog.urls')),
    path('account/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler400 = 'core.error_views.bad_request'
handler403 = 'core.error_views.permission_denied'
handler404 = 'core.error_views.page_not_found'
handler500 = 'core.error_views.server_error'
