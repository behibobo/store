# Generated by Django 2.2.4 on 2020-03-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_itemspec_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=300, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('content', models.CharField(blank=True, max_length=300, null=True)),
                ('link', models.CharField(blank=True, max_length=300, null=True)),
                ('order', models.IntegerField(default=1)),
                ('display', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField()),
                ('finish_date', models.DateTimeField()),
            ],
        ),
    ]
