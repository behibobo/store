# Generated by Django 2.2.4 on 2020-06-12 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_auto_20200609_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
