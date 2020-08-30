from django_countries.serializer_fields import CountryField
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from core.models import (
    Address, ItemImage, Category, Option, Wishlist, Brand, UserProfile, Upload, Item, Order, OrderItem, Coupon, Variation, ItemVariation,
    Payment, ItemSpec, Seo, Tag,
)
from panel.serializers import SeoSerializer, TagsSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
            model = UserProfile
            fields = ('username', 'status', 'credit_based_user', 'credit', 'credit_confirmed')
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
            'image',
            'thumbnail',
            'alt',
            'title'
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
    seo = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'slug',
            'display',
            'image',
            'seo',
            'tags',
            'doc'
        )

    def get_seo(self, obj):
        seo = Seo.objects.filter(item_id=obj.id).filter(item_type='brand').first()
        if seo:
            return SeoSerializer(seo).data
        else:
            return None

    def get_tags(self, obj):
        tags = Tag.objects.filter(item_id=obj.id).filter(item_type='brand')
        names = [tag.name for tag in tags]
        if tags:
            return names
        else:
            return None


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
            'doc'

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


class SimpleItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'image',

        )

    def get_image(self, obj):
        return ItemImageSerializer(obj.images.order_by('order').first()).data


class SingleCategoryAndProductSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image',
            'items',
        )
    
    def get_items(self, obj):
        return SimpleItemSerializer(obj.products.all()[0:10], many=True).data

class CartItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(read_only=True)
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
            'image',
        )

    def get_category(self, obj):
        return SingleCategorySerializer(obj.category).data

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data

    def get_image(self, obj):
        return ItemImageSerializer(obj.images.order_by('order').first()).data



class SingleItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    wishlist = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(read_only=True)
    variations = serializers.SerializerMethodField()
    category_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()
    seo = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()
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
            'specs',
            'seo',
            'tags',
            'doc'
        )

    def get_category(self, obj):
        return SingleCategorySerializer(obj.category).data

    def get_specs(self, obj):
        return ItemSpecSerializer(ItemSpec.objects.filter(item_id = obj.id), many=True).data

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data

    def get_images(self, obj):
        return ItemImageSerializer(obj.images.order_by('order').all(), many=True).data

    def get_variations(self, obj):
        return VariationSerializer(obj.variations.all(), many=True).data

    def get_wishlist(self, obj):
        return Wishlist.objects.filter(item_id=obj.id).exists()

    def get_seo(self, obj):
        seo = Seo.objects.filter(item_id=obj.id).filter(item_type='item').first()
        if seo:
            return SeoSerializer(seo).data
        else:
            return None
    
    def get_tags(self, obj):
        tags = Tag.objects.filter(item_id=obj.id).filter(item_type='item')
        names = [tag.name for tag in tags]
        if tags:
            return names
        else:
            return None

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
    variation = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'variation',
            'item',
            'quantity',
            'final_price'
        )

    def get_item(self, obj):
        return ItemSerializer(obj.item).data

    def get_variation(self, obj):
        return VariationSerializer(obj.variation).data
    
    def get_item(self, obj):
        return CartItemSerializer(obj.variation.item).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_items',
            'total',
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.order_items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()


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
    user_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    province_id = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    class Meta:
        model = Address
        fields = (
            'id',
            'user_id',
            'address',
            'city_id',
            'province_id',
            'zip',
            'name',
            'mobile',
            'default',
            'city_name',
            'province_name',
        )
    
    def get_province_name(self, obj):
        return obj.city.province.name
    
    def get_city_name(self, obj):
        return obj.city.name

    def get_province_id(self, obj):
        return obj.city.province.id


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
    seo = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
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
            'children',
            'seo',
            'tags',
            'svg_icon'
        )

    def get_seo(self, obj):
        seo = Seo.objects.filter(item_id=obj.id).filter(item_type='category').first()
        if seo:
            return SeoSerializer(seo).data
        else:
            return None

    def get_tags(self, obj):
        tags = Tag.objects.filter(item_id=obj.id).filter(item_type='category')
        names = [tag.name for tag in tags]
        if tags:
            return names
        else:
            return None



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

class CompareListSerializer(serializers.ModelSerializer):
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