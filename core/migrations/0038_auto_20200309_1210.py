# Generated by Django 2.2.4 on 2020-03-09 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_slider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='slider',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
