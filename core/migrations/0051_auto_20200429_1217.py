# Generated by Django 2.2.4 on 2020-04-29 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_auto_20200428_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
