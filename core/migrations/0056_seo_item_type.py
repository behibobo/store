# Generated by Django 2.2.4 on 2020-06-04 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_article_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='seo',
            name='item_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
