# Generated by Django 2.2.4 on 2020-01-29 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20200129_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='option_one',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='variation',
            name='option_three',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='variation',
            name='option_two',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]