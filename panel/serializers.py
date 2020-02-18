from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from core.models import (
    Address, Upload, Option, Brand, Category, Wishlist, Item, ItemImage, Order, OrderItem, Coupon, Variation, ItemVariation,
    Payment, Variation
)



class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = (
            'id',
            'file_path'
        )


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = (
            'id',
            'item_id',
            'order',
            'image'
        )

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            'id',
            'name'
        )

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'slug',
            'display',
            'image'
        )

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only= True)
    class Meta:
        model = Category
        fields = (
            'id',
            'order',
            'name',
            'slug',
            'display',
            'parent',
            'image',
            'children'
        )

class SingleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image'
        )

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(read_only=True)
    variations = serializers.SerializerMethodField()
    category_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()
    wishlist = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'category',
            'category_id',
            'brand',
            'brand_id',
            'slug',
            'description',
            'images',
            'variations',
            'wishlist'
        )

    def get_category(self, obj):
        return SingleCategorySerializer(obj.category).data

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data

    def get_images(self, obj):
        return ItemImageSerializer(obj.images.all(), many=True).data

    def get_variations(self, obj):
        return VariationSerializer(obj.variations.order_by('order').all(), many=True).data

    def get_wishlist(self, obj):
        return Wishlist.objects.filter(item_id=obj.id).exists()

class ItemImagesSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Item
        fields = (
            'images',
        )

    def get_images(self, obj):
        return ItemImageSerializer(obj.images.all().order_by('order'), many=True).data

class VariationSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
    class Meta:
        model = Variation
        fields = (
            'id',
            'item_id',
            'stock',
            'price',
            'reduced_price',
            'option_one',
            'value_one',
            'option_two',
            'value_two',
            'option_three',
            'value_three',
        )
