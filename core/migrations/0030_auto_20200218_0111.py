# Generated by Django 2.2.4 on 2020-02-17 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_variation_main'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='main',
        ),
        migrations.AddField(
            model_name='variation',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
