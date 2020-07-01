from django_countries import countries
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
import csv
import os
from home.settings.base import BASE_DIR

from .serializers import (
    ItemSerializer,
    CategorySerializer,
    SingleCategorySerializer,
    UploadSerializer,
    BrandSerializer,
    ItemImagesSerializer,
    ItemImageSerializer,
    OptionSerializer,
    SpecSerializer,
    VariationSerializer,
    CategorySerializer,
    CategorySpecSerializer,
    ItemSpecSerializer,
    SliderSerializer,
    ItemOptionSerializer,
    ArticleSerializer,
    SeoSerializer,
    PageSerializer,
    SettingSerializer,
    MenuSerializer,
    TagSerializer,
)
from core.models import (
    Item, 
    CategorySpec, 
    ItemSpec, 
    Article, 
    Brand, 
    Spec, 
    Variation, 
    ItemImage, 
    Upload, 
    Category, 
    OrderItem, 
    Option, 
    Order, 
    Address, 
    Payment, 
    Coupon, 
    Refund, 
    UserProfile,
    Variation, 
    ItemVariation, 
    Slider, 
    ItemOption, 
    Province, 
    City, 
    Seo, 
    Page, 
    Setting,
    Menu,
    Tag,
    )


# class ImportCities(APIView):
#     def get(self, request, format=None):
#         province_path = os.path.join(BASE_DIR, "province.csv")
#         city_path = os.path.join(BASE_DIR, "city.csv")
#         Province.objects.all().delete()
#         City.objects.all().delete()
#         with open(province_path) as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 province = Province.objects.create(
#                     name=row[1],
#                     )
#                 with open(city_path) as ff:
#                     rreader = csv.reader(ff)
#                     for rrow in rreader: 
#                         if rrow[1] == row[0]:
#                             city = City.objects.create(
#                                 province_id = province.id,
#                                 name=rrow[3],
#                             )

#         return Response([], status=status.HTTP_201_CREATED)



class UploadList(APIView):
    def post(self, request, format=None):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemUploadList(APIView):
    def post(self, request, pk, format=None):
        images = dict((request.data).lists())['file_path']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(img_name)
            file_serializer = UploadSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                im = ItemImage(item_id=pk, image=file_serializer.data['file_path'])
                im.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        item = Item.objects.get(pk=pk)
        serializer = ItemImagesSerializer(item)
        return Response(serializer.data)

class ItemUploadDetail(APIView):
    def get_object(self, pk, id):
        try:
            return ItemImage.objects.get(pk=id)
        except Variation.DoesNotExist:
            raise Http404

    def get(self, request, pk, id,format=None):
        image = self.get_object(pk, id)
        serializer = ItemImageSerializer(image)
        return Response(serializer.data)


    def put(self, request, pk, id, format=None):
        image = self.get_object(pk, id)
        serializer = ItemImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, id, format=None):
        upload = self.get_object(pk, id)
        upload.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadSort(APIView):
    def post(self, request, pk, format=None):
        uploads = request.data
        data = uploads["uploads"]
        for index, item in enumerate(data):
            image = ItemImage.objects.get(pk=item)
            image.order = index
            image.save()
        product = Item.objects.get(pk=pk)
        serializer = ItemImagesSerializer(product)
        return Response(serializer.data)

class UploadDelete(DestroyAPIView):
    def delete(self, request, pk, id, format=None):
        image = ItemImage.objects.get(pk=id)
        image.delete()
        return Response(status=HTTP_200_OK)



class UploadDetail(APIView):

    def get_object(self, pk):
        try:
            return Upload.objects.get(pk=pk)
        except Upload.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        upload = self.get_object(pk)
        serializer = UploadSerializer(upload)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        upload = self.get_object(pk)
        upload.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.filter(display=True).filter(parent__isnull=True).order_by('order')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']
                seo_data['item_type'] = "category"
                seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "category", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryOrder(APIView):
    def post(self, request, format=None):
        items = request.data
        print(items[0]['parentId'])
        for item in items:
            cat = Category.objects.get(pk=item['id'])
            cat.parent_id = item['parentId']
            cat.order = item['order']
            cat.save()

        return Response([], status=status.HTTP_201_CREATED)

class CategoryDetail(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']

                seo = Seo.objects.filter(item_id=serializer.data['id']).filter(item_type='category').first()
                if seo:
                    seo_serializer = SeoSerializer(seo, data=seo_data)
                else:
                    seo_data['item_type'] = "category"
                    seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                Tag.objects.filter(item_id=serializer.data['id']).filter(item_type='category').delete()
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "category", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ArticleList(APIView):
    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']
                seo_data['item_type'] = "article"
                seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "article", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticleDetail(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(category)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']

                seo = Seo.objects.filter(item_id=serializer.data['id']).filter(item_type='article').first()
                if seo:
                    seo_serializer = SeoSerializer(seo, data=seo_data)
                else:
                    seo_data['item_type'] = "article"
                    seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                Tag.objects.filter(item_id=serializer.data['id']).filter(item_type='article').delete()
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "article", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class BrandList(APIView):

    def get(self, request, format=None):
        brands = Brand.objects.filter(display=True)
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']
                seo_data['item_type'] = "brand"
                seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "brand", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BrandDetail(APIView):

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']

                seo = Seo.objects.filter(item_id=serializer.data['id']).filter(item_type='brand').first()
                if seo:
                    seo_serializer = SeoSerializer(seo, data=seo_data)
                else:
                    seo_data['item_type'] = "brand"
                    seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                Tag.objects.filter(item_id=serializer.data['id']).filter(item_type='brand').delete()
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "brand", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        brand = self.get_object(pk)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserIDView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'userID': request.user.id}, status=HTTP_200_OK)


class ItemList(APIView):

    def get(self, request, format=None):
        items = Item.objects.order_by('-created_at')
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']
                seo_data['item_type'] = "item"
                seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "item", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(APIView):

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']

                seo = Seo.objects.filter(item_id=serializer.data['id']).filter(item_type='item').first()
                if seo:
                    seo_serializer = SeoSerializer(seo, data=seo_data)
                else:
                    seo_data['item_type'] = "item"
                    seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                Tag.objects.filter(item_id=serializer.data['id']).filter(item_type='item').delete()
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "item", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemOptionList(APIView):
    def get(self, request, pk, format=None):
        options = {}
        result = []
        items = ItemOption.objects.filter(item_id=pk)
        for item in items:
            if item.option not in options.keys():
                options[str(item.option)] = [item.value]
            elif item.value not in options[str(item.option)]:
                options[str(item.option)].append(item.value)

        for k , v in options.items():
            result.append({"key": k, "values": v})

        return Response(result)

    def post(self, request, pk, format=None):
        data = request.data
        ItemOption.objects.filter(item_id = pk).delete()
        for index, item in enumerate(data):
            for val in item['values']:
                o = ItemOption()
                o.item_id = pk
                o.option = item['key']
                o.value = val
                o.save()
        return Response(status=status.HTTP_201_CREATED)

class VariationList(APIView):
    def get(self, request, pk, format=None):
        variations = Variation.objects.filter(item_id=pk)
        serializer = VariationSerializer(variations, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = VariationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VariationDetail(APIView):

    def get_object(self, pk, id):
        try:
            return Variation.objects.get(pk=id)
        except Variation.DoesNotExist:
            raise Http404

    def get(self, request, pk, id,format=None):
        variation = self.get_object(pk, id)
        serializer = VariationSerializer(variation)
        return Response(serializer.data)


    def put(self, request, pk, id, format=None):
        variation = self.get_object(pk, id)
        serializer = VariationSerializer(variation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, id, format=None):
        variation = self.get_object(pk, id)
        variation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OptionList(APIView):

    def get(self, request, format=None, *args, **kwagrs):
        options_one = Variation.objects.all().values('option_one', 'option_two', 'option_three')
        options_two = ItemOption.objects.all().values('option')
        data = []
        for item in options_one:
            if item['option_one'] is not None and item['option_one'] not in data and item['option_one'].startswith(request.query_params.get('keyword', "")):
                data.append(item['option_one'])
            if item['option_two'] is not None and item['option_two'] not in data and item['option_two'].startswith(request.query_params.get('keyword', "")):
                data.append(item['option_two'])
            if item['option_three'] is not None and item['option_three'] not in data and item['option_three'].startswith(request.query_params.get('keyword', "")):
                data.append(item['option_three'])

        for item in options_two:
            if item['option'] is not None and item['option'] not in data and item['option'].startswith(request.query_params.get('keyword', "")):
                data.append(item['option'])

        return JsonResponse(data, safe=False)

    def post(self, request, format=None):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecList(APIView):

    def get(self, request, format=None, *args, **kwagrs):
        specs = Spec.objects.filter(name__startswith=request.query_params.get('keyword', ""))
        serializer = SpecSerializer(specs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SpecSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecDetail(APIView):
    def get_object(self, pk):
        try:
            return Spec.objects.get(pk=pk)
        except Spec.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print("here")
        spec = self.get_object(pk)
        serializer = SpecSerializer(spec)
        return Response(serializer.data)


    def put(self, request, pk,  format=None):
        spec = self.get_object(pk)
        serializer = SpecSerializer(spec, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        variation = self.get_object(pk)
        variation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ValueList(APIView):
    def get(self, request, format=None, *args, **kwagrs):
        opt = request.query_params.get('option', "")
        values = Variation.objects.filter(Q(option_one=opt) | Q(option_two=opt) | Q(option_three=opt)).values('value_one', 'value_two', 'value_three')
        values_two = ItemOption.objects.filter(option=opt).values('value')
        data = []
        for item in values:
            if item['value_one'] is not None and item['value_one'] not in data and item['value_one'].startswith(request.query_params.get('keyword', "")):
                data.append(item['value_one'])
            if item['value_two'] is not None and item['value_two'] not in data and item['value_two'].startswith(request.query_params.get('keyword', "")):
                data.append(item['value_two'])
            if item['value_three'] is not None and item['value_three'] not in data and item['value_three'].startswith(request.query_params.get('keyword', "")):
                data.append(item['value_three'])

        for item in values_two:
            if item['value'] is not None and item['value'] not in data and item['value'].startswith(request.query_params.get('keyword', "")):
                data.append(item['value'])

        return JsonResponse(data, safe=False)


class OptionDetail(APIView):

    def get_object(self, pk):
        try:
            return Option.objects.get(pk=pk)
        except Option.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        option = self.get_object(pk)
        serializer = OptionSerializer(option)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        option = self.get_object(pk)
        serializer = OptionSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        option = self.get_object(pk)
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategorySpecList(APIView):
    def get(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySpecSerializer(category.specs, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
        serializer = CategorySpecSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            category = Category.objects.get(pk=pk)
            serializer = CategorySpecSerializer(category.specs, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategorySpecDetail(APIView):
    def get_object(self,pk):
        try:
            return CategorySpec.objects.get(pk=pk)
        except CategorySpec.DoesNotExist:
            raise Http404

    def delete(self, request, pk, id, format=None):
        item = self.get_object(id)
        item.delete()
        category = Category.objects.get(pk=pk)
        serializer = CategorySpecSerializer(category.specs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemSpecList(APIView):
    def get(self, request, pk, format=None):
        product = Item.objects.get(pk=pk)
        specs = CategorySpec.objects.filter(category_id=product.category_id)
        for item in specs:
            if not ItemSpec.objects.filter(item_id=product.id).filter(spec=item.spec).exists():
                s = ItemSpec()
                s.item_id = product.id
                s.spec = item.spec
                s.value = ""
                s.save()
        serializer = ItemSpecSerializer(product.specs, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        for item in request.data:
            sp = ItemSpec.objects.filter(item_id=product.id).filter(spec=item['spec']).first()
            sp.value = item['value']
            sp.save()
        serializer = ItemSpecSerializer(product.specs, many=True)
        return Response(serializer.data)


class SliderList(APIView):
    def get(self, request, format=None):
        sliders = Slider.objects.order_by('order')
        serializer = SliderSerializer(sliders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SliderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SliderDetail(APIView):

    def get_object(self, pk):
        try:
            return Slider.objects.get(pk=pk)
        except Slider.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        slider = self.get_object(pk)
        serializer = SliderSerializer(slider)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        slider = self.get_object(pk)
        serializer = SliderSerializer(slider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        slider = self.get_object(pk)
        slider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SliderToggle(APIView):
    def get(self, request, pk, format=None):
        slider = Slider.objects.get(pk=pk)
        slider.display = not slider.display
        slider.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SliderSort(APIView):
    def post(self, request, format=None):
        data = request.data
        data = data["ids"]
        for index, item in enumerate(data):
            slider = Slider.objects.get(pk=item)
            slider.order = index
            slider.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

def modify_input_for_multiple_files(image):
    dict = {}
    dict['file_path'] = image
    return dict

class SettingList(APIView):
    def get(self, request, format=None):
        setting = Setting.objects.first()

        if not setting:
            setting = Setting()
            setting.save()
        serializer = SettingSerializer(setting, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        setting = Setting.objects.first()

        if not setting:
            setting = Setting()
            setting.save()

        serializer = SettingSerializer(setting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageList(APIView):
    def get(self, request, format=None):
        pages = Page.objects.all()
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']
                seo_data['item_type'] = "page"
                seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "page", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PageDetail(APIView):

    def get_object(self, pk):
        try:
            return Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        page = self.get_object(pk)
        serializer = PageSerializer(page)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        page = self.get_object(pk)
        serializer = PageSerializer(page, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if "seo" in request.data and request.data["seo"] is not None:
                seo_data = request.data["seo"]
                seo_data['item_id'] = serializer.data['id']

                seo = Seo.objects.filter(item_id=serializer.data['id']).filter(item_type='page').first()
                if seo:
                    seo_serializer = SeoSerializer(seo, data=seo_data)
                else:
                    seo_data['item_type'] = "page"
                    seo_serializer = SeoSerializer(data=seo_data)
                if seo_serializer.is_valid():
                    seo_serializer.save()

            if "tags" in request.data and request.data["tags"] is not None:
                tags = request.data["tags"]
                Tag.objects.filter(item_id=serializer.data['id']).filter(item_type='page').delete()
                for tag in tags:
                    tag_data = {"item_id": serializer.data['id'], "item_type": "page", "name": tag}
                    tag_serializer = TagSerializer(data=tag_data)
                    if tag_serializer.is_valid():
                        tag_serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        page = self.get_object(pk)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MenuList(APIView):
    def get(self, request, format=None):
        menu = Menu.objects.filter(display=True).order_by('order')
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MenuDetail(APIView):

    def get_object(self, pk):
        try:
            return Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        menu = self.get_object(pk)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):
    def get(self, request, format=None, *args, **kwagrs):
        keyword = request.query_params.get('tag', "")
        tags = Tag.objects.filter(name__startswith=keyword).distinct("name")
        data = [tag.name for tag in tags]
        return JsonResponse(data, safe=False)