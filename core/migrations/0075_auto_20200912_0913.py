# Generated by Django 2.2.4 on 2020-09-12 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_auto_20200912_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='url',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]