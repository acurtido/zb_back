from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from zb_backend.catalog.models import Brand, Product, ProductTrack
from zb_backend.catalog.serializers import (BrandSerializer, GroupSerializer,
                                             ProductSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.AllowAny()]

        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        product_track_queryset = ProductTrack.objects.select_for_update().filter(
            product=instance)

        with transaction.atomic():
            product_track = product_track_queryset.first()
            product_track.visits += 1
            product_track.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
