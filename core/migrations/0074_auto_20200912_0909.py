# Generated by Django 2.2.4 on 2020-09-12 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0073_auto_20200912_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='url',
            field=models.SlugField(blank=True, null=True),
        ),
    ]