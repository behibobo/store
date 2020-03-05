from django_countries.serializer_fields import CountryField
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from core.models import (
    Address, ItemImage, Category, Option, Wishlist, Brand, UserProfile, Upload, Item, Order, OrderItem, Coupon, Variation, ItemVariation,
    Payment, ItemSpec,
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
            model = UserProfile
            fields = ('username', 'status')
            read_only_fields = ('email',)

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = (
            'id',
            'code',
            'amount'
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
            'image'
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

class SingleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
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

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()
    variation = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()
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
            'image',
            'variation',
            'wishlist',
            'specs',
        )

    def get_category(self, obj):
        return SingleCategorySerializer(obj.category).data

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data

    def get_image(self, obj):
        return ItemImageSerializer(obj.images.order_by('order').first()).data

    def get_variation(self, obj):
        variant = obj.variations.order_by('order').first()
        if variant:
            return VariationSerializer(variant).data
        return None

    def get_wishlist(self, obj):
        return Wishlist.objects.filter(item_id=obj.id).exists()
    
    def get_specs(self, obj):
        return ItemSpecSerializer(ItemSpec.objects.filter(item_id = obj.id), many=True).data




class SingleItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    wishlist = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(read_only=True)
    variations = serializers.SerializerMethodField()
    category_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()
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
            'wishlist',
        )

    def get_category(self, obj):
        return SingleCategorySerializer(obj.category).data

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data

    def get_images(self, obj):
        return ItemImageSerializer(obj.images.order_by('order').all(), many=True).data

    def get_variations(self, obj):
        return VariationSerializer(obj.variations.all(), many=True).data

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

class OrderItemSerializer(serializers.ModelSerializer):
    item_variations = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'item',
            'item_variations',
            'quantity',
            'final_price'
        )

    def get_item(self, obj):
        return ItemSerializer(obj.item).data

    def get_item_variations(self, obj):
        return ItemVariationDetailSerializer(obj.item_variations.all(), many=True).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_items',
            'total',
            'coupon'
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()

    def get_coupon(self, obj):
        if obj.coupon is not None:
            return CouponSerializer(obj.coupon).data
        return None


class ItemVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVariation
        fields = (
            'id',
            'value',
            'attachment'
        )


class ItemDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    variations = serializers.SerializerMethodField()

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
            'image',
            'variations'
        )

    def get_category(self, obj):
        return obj.get_category_display()

    def get_label(self, obj):
        return obj.get_label_display()

    def get_variations(self, obj):
        return VariationSerializer(obj.variation_set.all(), many=True).data


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'street_address',
            'apartment_address',
            'country',
            'zip',
            'address_type',
            'default'
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'amount',
            'timestamp'
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


class ItemSpecSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
    class Meta:
        model = ItemSpec
        fields = (
            'id',
            'item_id',
            'spec',
            'value',
        )