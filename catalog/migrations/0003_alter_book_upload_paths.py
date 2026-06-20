from django.db import migrations, models

import catalog.utils


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_book_cover_file_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(
                blank=True,
                help_text='Kompyuterdan muqova rasmini yuklang (ixtiyoriy)',
                upload_to=catalog.utils.book_cover_upload_path,
                verbose_name='Muqova fayli',
            ),
        ),
        migrations.AlterField(
            model_name='book',
            name='pdf_file',
            field=models.FileField(
                blank=True,
                help_text='Kompyuterdan PDF fayl yuklang (ixtiyoriy)',
                upload_to=catalog.utils.book_pdf_upload_path,
                verbose_name='PDF fayl',
            ),
        ),
    ]
