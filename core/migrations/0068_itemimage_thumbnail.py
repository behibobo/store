# Generated by Django 2.2.4 on 2020-07-11 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_auto_20200612_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemimage',
            name='thumbnail',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
