from django.db import models


NUTRITION_GRADES = [
    ('', 'N/A'),
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
]


class Store(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    slug = models.SlugField(verbose_name='slug', max_length=200)


class Category(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    slug = models.SlugField(verbose_name='slug', max_length=200)


class Product(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    ingredients = models.CharField(verbose_name='ingredients', max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')
    sub_category = models.ManyToManyField(
        Category,
        verbose_name='sub_category',
        blank=True,
    )
    store = models.ManyToManyField(
        Store,
        verbose_name="store",
        blank=True,
    )
    nutrition_grade = models.CharField(
        max_length=1,
        choices=NUTRITION_GRADES,
        default='',
    )


class Favorite(models.Model):
    product = models.ForeignKey('Product', related_name='product', on_delete=models.CASCADE)
    substitute = models.ForeignKey('Product', related_name='substitute', on_delete=models.CASCADE)
