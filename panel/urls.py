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
    UploadDelete,
    SpecList,
    CategorySpecDetail,
    CategorySpecList,
    ItemSpecList,
    SliderList,
    SliderDetail,
    SliderToggle,
    SliderSort,
    ItemOptionList,
    ArticleDetail,
    ArticleList,
    SettingList,
    PageList,
    PageDetail,
    MenuList,
    MenuDetail,
    TagList,
)

urlpatterns = [
    path('options/', OptionList.as_view(), name='admin-option'),
    path('specs/', SpecList.as_view(), name='admin-specs'),
    path('values/', ValueList.as_view(), name='admin-values'),
    path('tags/', TagList.as_view(), name='admin-tags'),
    path('options/<int:pk>/', OptionDetail.as_view(), name='admin-option-get'),
    path('categories/', CategoryList.as_view(), name='admin-category'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='admin-category-get'),
    path('articles/', ArticleList.as_view(), name='admin-articles'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='admin-article-get'),
    path('products/', ItemList.as_view(), name='admin-items'),
    path('products/<int:pk>/', ItemDetail.as_view(), name='admin-item-get'),
    path('products/<int:pk>/variations/', VariationList.as_view(), name='admin-product-variations'),
    path('products/<int:pk>/variations/<int:id>/', VariationDetail.as_view(), name='admin-product-variations-get'),
    path('products/<int:pk>/specs/', ItemSpecList.as_view(), name='admin-product-specs'),
    path('products/<int:pk>/options/', ItemOptionList.as_view(), name='admin-product-options'),
    path('brands/', BrandList.as_view(), name='admin-brand'),
    path('brands/<int:pk>/', BrandDetail.as_view(), name='admin-brand-get'),
    path('uploads/', UploadList.as_view(), name='admin-upload'),
    path('products/<int:pk>/uploads/', ItemUploadList.as_view(), name='admin-upload'),
    path('products/<int:pk>/uploads/sort/', UploadSort.as_view(), name='admin-upload-sort'),
    path('products/<int:pk>/uploads/<int:id>/delete/', UploadDelete.as_view(), name='admin-upload-sort'),
    path('uploads/<int:pk>/', UploadDetail.as_view(), name='admin-upload-get'),
    path('categories/<int:pk>/specs/', CategorySpecList.as_view(), name='admin-category-specs'),
    path('categories/<int:pk>/specs/<int:id>/', CategorySpecDetail.as_view(), name='admin-category-specs-get'),
    path('sliders/', SliderList.as_view(), name='admin-sliders'),
    path('sliders/<int:pk>/', SliderDetail.as_view(), name='admin-slider-get'),
    path('sliders/<int:pk>/toggle', SliderToggle.as_view(), name='admin-slider-toggle'),
    path('slider/sort/', SliderSort.as_view(), name='admin-slider-order'),
    path('setting/', SettingList.as_view(), name='admin-setting'),
    path('pages/', PageList.as_view(), name='admin-pages'),
    path('pages/<int:pk>/', PageDetail.as_view(), name='admin-page-get'),
    path('menus/', MenuList.as_view(), name='admin-menus'),
    path('menus/<int:pk>/', MenuDetail.as_view(), name='admin-menu-get'),
]
