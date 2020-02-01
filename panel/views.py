from django_countries import countries
from django.db.models import Q
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
from .serializers import (
    ItemSerializer,
    CategorySerializer,
    SingleCategorySerializer,
    UploadSerializer,
    BrandSerializer,
    ItemImagesSerializer,
    OptionSerializer,
    VariationSerializer,
)
from core.models import Item, Brand, ItemImage, Upload, Category, OrderItem, Option, Order, Address, Payment, Coupon, Refund, UserProfile, Variation, ItemVariation

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
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
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
        options = Option.objects.filter(name__startswith=request.query_params.get('keyword', ""))
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

def modify_input_for_multiple_files(image):
    dict = {}
    dict['file_path'] = image
    return dict