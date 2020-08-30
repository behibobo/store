# Generated by Django 2.2.4 on 2020-06-09 13:32

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_auto_20200607_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, max_length=1000, unique=True),
        ),
    ]
