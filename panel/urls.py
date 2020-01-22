from django.urls import path
from .views import (
    ItemDetail,
    ItemList,
    CategoryDetail,
    CategoryList,
    UploadDetail,
    UploadList,
    BrandDetail,
    BrandList
)

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='admin-category'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='admin-category-get'),
    path('products/', ItemList.as_view(), name='admin-items'),
    path('products/<int:pk>/', ItemDetail.as_view(), name='admin-item-get'),
    path('brands/', BrandList.as_view(), name='admin-brand'),
    path('brands/<int:pk>/', BrandDetail.as_view(), name='admin-brand-get'),
    path('uploads/', UploadList.as_view(), name='admin-upload'),
    path('uploads/<int:pk>/', UploadDetail.as_view(), name='admin-upload-get'),
]
