# Generated by Django 2.2.4 on 2020-02-19 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_spec'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='core.Category')),
            ],
        ),
    ]
