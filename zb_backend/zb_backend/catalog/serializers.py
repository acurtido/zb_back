from django.contrib.auth.models import User, Group
from zb_backend.catalog.models import Product, ProductTrack, Brand
from django.db import transaction
from rest_framework import serializers



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'price', 'brand']

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            ProductTrack.objects.create(product=instance)

        return instance
