# Generated by Django 2.2.4 on 2020-01-11 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200111_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Upload'),
        ),
    ]
