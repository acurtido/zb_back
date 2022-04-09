from django.db import models

class Brand(models.Model):
    name = models.CharField(null=False, max_length=50)

class Product(models.Model):
    sku = models.CharField(null=False, max_length=10, unique=True)
    name = models.CharField(null=False, max_length=50)
    price = models.FloatField(null=False, default=0.0)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

class ProductTrack(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    visits = models.IntegerField(null=False, default=0)

    

