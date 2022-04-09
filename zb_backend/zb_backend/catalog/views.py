from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from zb_backend.catalog.models import Brand, Product, ProductTrack
from zb_backend.catalog.serializers import (BrandSerializer,
                                            ProductSerializer, UserSerializer)
from zb_backend.catalog.controllers.aws_ses_controller import send_mail


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
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

        data = {
            **serializer.data,
            "brand": instance.brand.name
        }

        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        users = User.objects.filter()

        for user in users:
            send_mail(recipient=user.email, user=request.user,
                      product=instance)

        return super().update(request, *args, **kwargs)
