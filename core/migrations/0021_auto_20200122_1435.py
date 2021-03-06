# Generated by Django 2.2.4 on 2020-01-22 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20200118_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.RemoveField(
            model_name='item',
            name='label',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='title',
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='core.Category'),
        ),
        migrations.AlterField(
            model_name='itemvariation',
            name='value',
            field=models.CharField(max_length=150),
        ),
    ]
