# Generated by Django 5.1.5 on 2025-01-27 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_app', '0003_adminparol'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminparol',
            options={'ordering': ['section'], 'verbose_name': 'Admin Password', 'verbose_name_plural': 'Admin Passwords'},
        ),
        migrations.AddField(
            model_name='adminparol',
            name='section',
            field=models.CharField(blank=True, choices=[('1', "Mexanika bo'limi"), ('2', 'Omborxona')], default='1', max_length=255, null=True),
        ),
    ]
