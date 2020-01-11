from django.urls import path
from .views import (
    ItemListView,
    CategoryDetail,
    CategoryList,
    UploadDetail,
    UploadList,
)

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='admin-category'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='admin-category-get'),
    path('uploads/', UploadList.as_view(), name='admin-upload'),
    path('uploads/<int:pk>/', UploadDetail.as_view(), name='admin-upload-get'),
]
