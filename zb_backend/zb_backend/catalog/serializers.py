from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from zb_backend.catalog.models import Brand, Product, ProductTrack


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['url', 'sku', 'name', 'price', 'brand', 'brand_name']

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            ProductTrack.objects.create(product=instance)

        return instance

    def get_brand_name(self, obj):
        return obj.brand.name


class ProductTrackSerializer(serializers.HyperlinkedModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()

    class Meta:
        model = ProductTrack
        fields = ['product', 'product_name', 'product_sku', 'visits']

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_sku(self, obj):
        return obj.product.sku
