# Generated by Django 2.2.4 on 2020-08-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_category_svg_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='credit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='credit_based_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='credit_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
