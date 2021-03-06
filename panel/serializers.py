from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from core.models import *
from jalali_date import datetime2jalali, date2jalali
import json
from django.contrib.auth.models import User, Group


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


class UploadSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(read_only=True)
    class Meta:
        model = Upload
        fields = (
            'id',
            'file_path',
            'thumbnail'
        )

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = (
            'id',
            'file_path',
        )


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = (
            'id',
            'item_id',
            'order',
            'image',
            'thumbnail',
            'alt',
            'title',
        )

class SeoSerializer(serializers.ModelSerializer):
    # item_id = serializers.SerializerMethodField()
    class Meta:
        model = Seo
        fields = (
            'id',
            'item_id',
            'item_type',
            'title',
            'keywords',
            'description',
            'extra',
        )
    # def get_item_id(self, obj):
    #     return obj.item_id

class TagSerializer(serializers.ModelSerializer):
    # item_id = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = (
            'id',
            'item_id',
            'item_type',
            'name',
        )
    # def get_item_id(self, obj):
    #     return obj.item_id

class TagsSerializer(serializers.ModelSerializer):
    # item_id = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = (
            'name',
        )
    # def get_item_id(self, obj):
    #     return obj.item_id

class ArticleSerializer(serializers.ModelSerializer):
    shamsi_date = serializers.SerializerMethodField(read_only=True)
    seo = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'body',
            'image',
            'slug',
            'created_at',
            'shamsi_date',
            'seo',
            'tags',
        )

    def get_shamsi_date(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d %H:%M:%S')

    def get_seo(self, obj):
        seo = Seo.objects.filter(item_id=obj.id).filter(item_type='article').first()
        if seo:
            return SeoSerializer(seo).data
        else:
            return None

    def get_tags(self, obj):
        tags = Tag.objects.filter(item_id=obj.id).filter(item_type='article')
        names = [tag.name for tag in tags]
        if tags:
            return names
        else:
            return None


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = (
            'id',
            'name'
        )


class CitySerializer(serializers.ModelSerializer):
    province_id = serializers.IntegerField()
    class Meta:
        model = City
        fields = (
            'id',
            'province_id',
            'name'
        )

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            'id',
            'name'
        )

class SpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spec
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
            'doc',
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
    seo = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
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
            'seo',
            'tags',
            'doc',
            'out_of_stock_sale',
        )

    def get_category(self, obj):
        return SingleCategorySerializer(obj.category).data

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data

    def get_images(self, obj):
        return ItemImageSerializer(obj.images.all(), many=True).data

    def get_variations(self, obj):
        return VariationSerializer(obj.variations.order_by('order').all(), many=True).data

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

class ItemOptionSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
    class Meta:
        model = ItemOption
        fields = (
            'id',
            'item_id',
            'option',
            'value',
        )

class CategorySpecSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    class Meta:
        model = CategorySpec
        fields = (
            'id',
            'category_id',
            'spec',
            'order',
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

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = (
            'id',
            'order',
            'title',
            'content',
            'display',
            'link',
            'image',
        )

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = (
            'id',
            'logo',
            'title',
            'keywords',
            'description',
            'ArticleCount',
            'ItemCount',
        )

class PageSerializer(serializers.ModelSerializer):
    seo = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'slug',
            'content',
            'image',
            'url',
            'seo',
            'tags',
        )

    def get_seo(self, obj):
        seo = Seo.objects.filter(item_id=obj.id).filter(item_type='page').first()
        if seo:
            return SeoSerializer(seo).data
        else:
            return None

    def get_tags(self, obj):
        tags = Tag.objects.filter(item_id=obj.id).filter(item_type='page')
        names = [tag.name for tag in tags]
        if tags:
            return names
        else:
            return None

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'id',
            'name',
            'url',
            'display',
            'order'
        )


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'status',
            'credit_based_user',
            'credit',
            'credit_confirmed'
        )

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
            'final_price',
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


class SingleUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'orders', 'addresses']

    def get_profile(self, obj):
        profile = UserProfile.objects.get(user_id=obj.id)
        return ProfileSerializer(profile).data

    def get_orders(self, obj):
        orders = Order.objects.filter(user_id=obj.id)
        return OrderSerializer(orders, many=True).data

    def get_addresses(self, obj):
        addresses = Address.objects.filter(user_id=obj.id)
        return AddressSerializer(addresses, many=True).data

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'orders']

    def get_profile(self, obj):
        profile = UserProfile.objects.get(user_id=obj.id)
        return ProfileSerializer(profile).data

    def get_orders(self, obj):
        orders = Order.objects.filter(user_id=obj.id)
        return len(orders)