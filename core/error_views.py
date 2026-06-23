from django.shortcuts import render


def _error_page(request, status, title, message, show_path=False):
    context = {
        'status_code': status,
        'error_title': title,
        'error_message': message,
    }
    if show_path:
        context['request_path'] = request.path
    return render(request, 'errors/error.html', context, status=status)


def page_not_found(request, exception):
    return _error_page(
        request,
        404,
        'Sahifa topilmadi',
        'Siz qidirayotgan sahifa mavjud emas, o\'chirilgan yoki manzili o\'zgartirilgan bo\'lishi mumkin.',
        show_path=True,
    )


def server_error(request):
    return _error_page(
        request,
        500,
        'Server xatosi',
        'Kechirasiz, texnik nosozlik yuz berdi. Iltimos, birozdan keyin qayta urinib ko\'ring yoki biz bilan bog\'laning.',
    )


def permission_denied(request, exception):
    return _error_page(
        request,
        403,
        'Kirish taqiqlangan',
        'Ushbu sahifaga kirish uchun ruxsatingiz yo\'q.',
    )


def bad_request(request, exception):
    return _error_page(
        request,
        400,
        'Noto\'g\'ri so\'rov',
        'So\'rovingizni qayta ishlash mumkin emas. Iltimos, ma\'lumotlarni tekshirib qayta urinib ko\'ring.',
    )
