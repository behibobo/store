# Generated by Django 2.2.4 on 2020-09-12 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_auto_20200912_0913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='url',
            new_name='page_url',
        ),
    ]
