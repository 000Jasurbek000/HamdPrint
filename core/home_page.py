"""Bosh sahifa — doimiy matnlar (faqat kitob soni bazadan olinadi)."""

HOME_INDEX_CATEGORIES = [
    {
        'slug': 'monografiyalar',
        'name': 'Monografiyalar',
        'description': 'Ilmiy-tadqiqot va monografik asarlarni nashr etamiz.',
    },
    {
        'slug': 'darsliklar',
        'name': 'Darsliklar',
        'description': "O'quv jarayonida foydalaniladigan zamonaviy darsliklar.",
    },
    {
        'slug': 'oquv-qollanmalar',
        'name': "O'quv qo'llanmalar",
        'description': "Talabalar va o'qituvchilar uchun qo'llanmalar.",
    },
    {
        'slug': 'oquv-methodik-qollanmalar',
        'name': "O'quv methodik qo'llanmalar",
        'description': "O'qitish metodikasi bo'yicha qo'llanmalar.",
    },
    {
        'slug': 'badiiy-adabiyotlar',
        'name': 'Badiiy adabiyotlar',
        'description': "Badiiy va ma'naviy-adabiy asarlar to'plami.",
    },
]


def get_home_categories_with_counts():
    from django.db.models import Count

    from catalog.models import Book

    count_map = {
        row['category__slug']: row['total']
        for row in Book.objects.values('category__slug').annotate(total=Count('id'))
        if row['category__slug']
    }
    return [
        {**cat, 'book_count': count_map.get(cat['slug'], 0)}
        for cat in HOME_INDEX_CATEGORIES
    ]
