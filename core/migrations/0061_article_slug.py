# Generated by Django 2.2.4 on 2020-06-04 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_page_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=''),
            preserve_default=False,
        ),
    ]
