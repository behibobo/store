# Generated by Django 2.2.4 on 2020-08-21 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_uploadfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='svg_icon',
            field=models.TextField(blank=True, null=True),
        ),
    ]
