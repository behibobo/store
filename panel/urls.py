from django.urls import path
from .views import (
    ItemDetail,
    ItemList,
    CategoryDetail,
    CategoryList,
    UploadDetail,
    UploadList,
    ItemUploadList,
    BrandDetail,
    BrandList,
    OptionList,
    OptionDetail,
    ValueList,
    VariationList,
    VariationDetail,
    UploadSort,
    SpecList,
    CategorySpecDetail,
    CategorySpecList,
    ItemSpecList,
)

urlpatterns = [
    path('options/', OptionList.as_view(), name='admin-option'),
    path('specs/', SpecList.as_view(), name='admin-specs'),
    path('values/', ValueList.as_view(), name='admin-values'),
    path('options/<int:pk>/', OptionDetail.as_view(), name='admin-option-get'),
    path('categories/', CategoryList.as_view(), name='admin-category'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='admin-category-get'),
    path('products/', ItemList.as_view(), name='admin-items'),
    path('products/<int:pk>/', ItemDetail.as_view(), name='admin-item-get'),
    path('products/<int:pk>/variations/', VariationList.as_view(), name='admin-product-variations'),
    path('products/<int:pk>/variations/<int:id>/', VariationDetail.as_view(), name='admin-product-variations-get'),
    path('products/<int:pk>/specs/', ItemSpecList.as_view(), name='admin-product-variations'),
    path('brands/', BrandList.as_view(), name='admin-brand'),
    path('brands/<int:pk>/', BrandDetail.as_view(), name='admin-brand-get'),
    path('uploads/', UploadList.as_view(), name='admin-upload'),
    path('products/<int:pk>/uploads/', ItemUploadList.as_view(), name='admin-upload'),
    path('products/<int:pk>/uploads/sort/', UploadSort.as_view(), name='admin-upload-sort'),
    path('uploads/<int:pk>/', UploadDetail.as_view(), name='admin-upload-get'),
    path('categories/<int:pk>/specs/', CategorySpecList.as_view(), name='admin-category-specs'),
    path('categories/<int:pk>/specs/<int:id>/', CategorySpecDetail.as_view(), name='admin-category-specs-get'),
]
