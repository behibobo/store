from django.urls import path
from .views import (
    ItemListView,
    CategoryDetail,
    CategoryList,
)

urlpatterns = [
    path('products/', ItemListView.as_view(), name='admin-product-list'),
    path('categories/', CategoryList.as_view(), name='admin-category'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='admin-category-get'),
]
