# Generated by Django 2.2.4 on 2020-02-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_itemspec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemspec',
            name='spec',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
