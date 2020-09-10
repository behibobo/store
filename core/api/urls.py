from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeList.as_view(), name='home-list'),
    path('user-id/', UserIDView.as_view(), name='user-id'),
    path('users/', UserList.as_view(), name='users'),
    path('provinces/', ProvinceList.as_view(), name='provinces'),
    path('provinces/<id>/cities/', CityList.as_view(), name='cities'),
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('addresses/', AddressList.as_view(), name='user-addresses'),
    path('addresses/<pk>/', AddressDetail.as_view(), name='user-addresses-get'),
    path('products/', ItemList.as_view(), name='product-list'),
    path('products/<str:slug>/', ItemDetail.as_view(), name='product-detail'),
    path('products/<str:slug>/wishlist/', WishlistToggle.as_view(), name='product-wishlist'),
    path('products/<str:slug>/specs/', ItemSpecList.as_view(), name='product-specs'),
    path('categories/', CategoryList.as_view(), name='category'),
    path('categories/<str:slug>/', CategoryDetail.as_view(), name='category-get'),
    path('brands/<str:slug>/', BrandDetail.as_view(), name='brand-get'),
    path('categories/<str:slug>/filters/', CategoryFilters.as_view(), name='category-filters'),
    path('brands/', BrandList.as_view(), name='brands'),
    path('brands/<str:slug>/', BrandDetail.as_view(), name='category-get'),
    path('compareList/', CompareList.as_view(), name='compare-items-get'),
    path('compareListItems/', CompareListItems.as_view(), name='compare-items-get'),
    path('search/', Search.as_view(), name='search-get'),
    path('keywordsearch/', KeywordSearch.as_view(), name='keyword-search-get'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', OrderDetailView.as_view(), name='cart'),
    path('checkout/', PaymentView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('order-item/<pk>/delete/',
         OrderItemDeleteView.as_view(), name='order-item-delete'),
    path('order-item/<pk>/update/',
         OrderQuantityUpdateView.as_view(), name='order-item-update'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('sliders/', SliderList.as_view(), name='slider-list'),
    path('same_category/', SameCategory.as_view(), name='same-category'),
    path('compare_list/', CompareList.as_view(), name='compare-list'),
    path('articles/', ArticleList.as_view(), name='articles'),
    path('articles/<slug>/', ArticleDetail.as_view(), name='article'),
    path('pages/', PageList.as_view(), name='pages'),
    path('pages/<slug>/', PageDetail.as_view(), name='page'),
    path('menus/', MenuList.as_view(), name='menus'),

]
