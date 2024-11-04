from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField('name',max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        db_table = 'category'


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField('name',max_length=100)
    description = models.TextField('description',default='')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='product_image/', blank=True)
    size = models.CharField('size', max_length=4, default='')
    season = models.CharField('season', max_length=100, blank=True)
    color = models.CharField('color', max_length=100, default='')
    fabric_type = models.CharField('fabric_type', max_length=512, blank=True)
    style = models.CharField('style', max_length=100, blank=True)
    brand = models.CharField('brand', max_length=100, blank=True)

    class Meta:
        db_table = 'product'


