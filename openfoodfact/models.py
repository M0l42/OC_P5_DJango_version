from django.db import models


NUTRITION_GRADES = [
    ('', 'N/A'),
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
]


class Category(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    tags = models.CharField(verbose_name='tags', max_length=200)
    url = models.CharField(verbose_name='url', max_length=200, blank=True)
    numbers_of_product = models.IntegerField(verbose_name="products", default=0, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='name', max_length=200, null=True)
    ingredients = models.CharField(verbose_name='ingredients', max_length=200, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category', null=True)
    store = models.TextField(verbose_name="store", blank=True, null=True)
    nutrition_grade = models.CharField(
        max_length=1,
        choices=NUTRITION_GRADES,
        default='',
        null=True
    )
    code = models.IntegerField(verbose_name="code", blank=True, default=0, null=True)
    url = models.TextField(verbose_name="url", blank=True, null=True)
    img_url = models.TextField(verbose_name="image_url", blank=True, null=True)
    fat_100 = models.FloatField(verbose_name="fat_100g", blank=True, default=0, null=True)
    fat_lvl = models.CharField(verbose_name="fat_lvl", blank=True, max_length=10, null=True)
    saturated_fat_100 = models.FloatField(verbose_name="saturated_fat_100g", blank=True, default=0, null=True)
    saturated_fat_lvl = models.CharField(verbose_name="saturated_fat_lvl", blank=True, max_length=10, null=True)
    sugar_100 = models.FloatField(verbose_name="sugar_100g", blank=True, default=0, null=True)
    sugar_lvl = models.CharField(verbose_name="sugar_lvl", blank=True, max_length=10, null=True)
    salt_100 = models.FloatField(verbose_name="salt_100g", blank=True, default=0, null=True)
    salt_lvl = models.CharField(verbose_name="salt_lvl", blank=True, max_length=10, null=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    product = models.ForeignKey('Product', related_name='product', on_delete=models.CASCADE)
    substitute = models.ForeignKey('Product', related_name='substitute', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='favorite_category', null=True)

    def __str__(self):
        return self.product.name
