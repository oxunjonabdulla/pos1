# Generated by Django 4.2.17 on 2025-01-24 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0013_kategoriya_nomi_ru_kategoriya_nomi_uz_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kategoriya',
            options={'ordering': ['nomi'], 'verbose_name': 'Kategoriya', 'verbose_name_plural': 'Kategoriyalar'},
        ),
    ]
