# Generated by Django 2.2.4 on 2020-06-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=1000, unique=True),
        ),
    ]