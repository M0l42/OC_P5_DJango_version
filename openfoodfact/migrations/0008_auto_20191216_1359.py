# Generated by Django 3.0 on 2019-12-16 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openfoodfact', '0007_auto_20191216_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ingredients',
            field=models.CharField(max_length=200, null=True, verbose_name='ingredients'),
        ),
    ]