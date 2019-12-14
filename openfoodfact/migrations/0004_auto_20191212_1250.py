# Generated by Django 3.0 on 2019-12-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openfoodfact', '0003_auto_20191211_2229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='slug',
            new_name='tags',
        ),
        migrations.AddField(
            model_name='category',
            name='numbers_of_product',
            field=models.IntegerField(default=0, null=True, verbose_name='products'),
        ),
        migrations.AddField(
            model_name='category',
            name='url',
            field=models.CharField(blank=True, max_length=200, verbose_name='slug'),
        ),
    ]