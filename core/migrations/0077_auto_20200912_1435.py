# Generated by Django 2.2.4 on 2020-09-12 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_auto_20200912_1433'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='page_url',
            new_name='url',
        ),
    ]
