# Generated by Django 2.2.4 on 2020-04-13 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20200402_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(allow_unicode=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(allow_unicode=True),
        ),
    ]
