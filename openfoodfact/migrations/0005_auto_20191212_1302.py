# Generated by Django 3.0 on 2019-12-12 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openfoodfact', '0004_auto_20191212_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='tags',
            field=models.CharField(max_length=200, verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.CharField(blank=True, max_length=200, verbose_name='url'),
        ),
    ]