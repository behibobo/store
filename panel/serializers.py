from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from core.models import (
    Address, Upload, Category, Item, Order, OrderItem, Coupon, Variation, ItemVariation,
    Payment
)


class ItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'price',
            'discount_price',
            'category',
            'label',
            'slug',
            'description',
            'image'
        )

    def get_category(self, obj):
        return obj.get_category_display()

    def get_label(self, obj):
        return obj.get_label_display()

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = (
            'id',
            'file_path'
        )

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_id = serializers.IntegerField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image_id',
            'image'
        )
    
    def get_image(self, obj):
        return UploadSerializer(obj.image).data
        


