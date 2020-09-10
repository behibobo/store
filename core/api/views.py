from django_countries import countries
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.utils.encoding import smart_str
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from core.models import Item, OrderItem, Order,Category, Brand
from .serializers import (
    ItemSerializer, OrderSerializer, ItemDetailSerializer, AddressSerializer,
    PaymentSerializer, CategorySerializer, BrandSerializer, SingleItemSerializer, ItemSpecSerializer,
    CompareListSerializer, SingleCategoryAndProductSerializer, BrandSerializer,
)
from panel.serializers import (
    SliderSerializer, ProvinceSerializer, CitySerializer, 
    ArticleSerializer, PageSerializer, SettingSerializer, 
    MenuSerializer,
)
from core.models import (
    Item, Wishlist, OrderItem,
    Order, ItemSpec, Address,
    Payment, Coupon, Refund,
    UserProfile, Variation,
    ItemVariation, Slider, ItemOption,
    Province,City, Article, Page, Setting, Menu,
    )


import stripe
import datetime
stripe.api_key = settings.STRIPE_SECRET_KEY

class ProvinceList(ListAPIView):
    def get(self, request, format=None):
        queryset = Province.objects.all()
        serializer = ProvinceSerializer(queryset, many=True)
        return Response(serializer.data)

class CityList(ListAPIView):
    def get(self, request, id, format=None):
        queryset = City.objects.filter(province_id=id)
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)

class UserIDView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'userID': request.user.id}, status=HTTP_200_OK)

class UserList(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        if User.objects.filter(username=username).exists():
            return Response({"message": "username already taken"}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, is_staff=False,
                                    password=password)
        user.save()
        user_profile = UserProfile.objects.get(user__id=user.pk)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'status': user_profile.status,
            'user_type': int(user.is_staff)
        })

# class ItemList(APIView):
#     def get(self, request, format=None):
#         permission_classes = (IsAuthenticated, )
#         items = Item.objects.all()
#         paginator = PageNumberPagination()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)


class ItemList(ListAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    pagination_class = PageNumberPagination


class ItemDetail(APIView):
    def get(self, request, slug, format=None):
        permission_classes = (IsAuthenticated, )
        items = Item.objects.get(slug=slug)
        serializer = SingleItemSerializer(items)
        return Response(serializer.data)


class OrderQuantityUpdateView(APIView):
    def post(self, request, pk, *args, **kwargs):
        quantity = request.data.get('quantity', None)


        if quantity is None:
            return Response({"message": "Invalid data"}, status=HTTP_400_BAD_REQUEST)


        order_Item = get_object_or_404(OrderItem, pk=pk)
        variation = get_object_or_404(Variation, pk=order_Item.variation_id)

        if quantity > variation.stock:
            return Response({"message": "More than Stock"}, status=HTTP_400_BAD_REQUEST)

        if(quantity == 0):
            order_Item.delete()
        else:
            order_Item.quantity = quantity
            order_Item.save()

        return Response(status=HTTP_200_OK)
        


class OrderItemDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, pk, *args, **kwargs):
        order_Item = get_object_or_404(OrderItem, pk=pk)
        order_Item.delete()
        order, found = Order.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):

        order, found = Order.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )

        variation_id = request.data.get('variation_id', None)
        quantity = request.data.get('quantity', None)
        if variation_id is None or quantity is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)

        variation = get_object_or_404(Variation, pk=variation_id)

        if quantity > variation.stock:
            return Response({"message": "More than Stock"}, status=HTTP_400_BAD_REQUEST)


        order_item_qs = OrderItem.objects.filter(
            variation=variation,
            order=order
        )

        if order_item_qs.exists():
            order_item = order_item_qs.first()
            order_item.quantity += quantity
            order_item.save()
        else:
            order_item = OrderItem.objects.create(
                variation=variation,
                order=order,
                quantity = quantity,
            )
            order_item.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        order, found = Order.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )
        return order
        # try:
        #     order = Order.objects.get(user=self.request.user, ordered=False)
        #     return order
        # except ObjectDoesNotExist:
        #     raise Http404("You do not have an active order")
        #     # return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)


class PaymentView(APIView):

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        userprofile = UserProfile.objects.get(user=self.request.user)
        token = request.data.get('stripeToken')
        billing_address_id = request.data.get('selectedBillingAddress')
        shipping_address_id = request.data.get('selectedShippingAddress')

        billing_address = Address.objects.get(id=billing_address_id)
        shipping_address = Address.objects.get(id=shipping_address_id)

        if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
            customer = stripe.Customer.retrieve(
                userprofile.stripe_customer_id)
            customer.sources.create(source=token)

        else:
            customer = stripe.Customer.create(
                email=self.request.user.email,
            )
            customer.sources.create(source=token)
            userprofile.stripe_customer_id = customer['id']
            userprofile.one_click_purchasing = True
            userprofile.save()

        amount = int(order.get_total() * 100)

        try:

                # charge the customer because we cannot charge the token more than once
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                customer=userprofile.stripe_customer_id
            )
            # charge once off on the token
            # charge = stripe.Charge.create(
            #     amount=amount,  # cents
            #     currency="usd",
            #     source=token
            # )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.billing_address = billing_address
            order.shipping_address = shipping_address
            # order.ref_code = create_ref_code()
            order.save()

            return Response(status=HTTP_200_OK)

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            return Response({"message": "{}".format(err.get('message'))}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return Response({"message": "Rate limit error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            print(e)
            # Invalid parameters were supplied to Stripe's API
            return Response({"message": "Invalid parameters"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return Response({"message": "Not authenticated"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return Response({"message": "Network error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return Response({"message": "Something went wrong. You were not charged. Please try again."}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            # send an email to ourselves
            return Response({"message": "A serious error occurred. We have been notifed."}, status=HTTP_400_BAD_REQUEST)

        return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)


class AddCouponView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        if code is None:
            return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        coupon = get_object_or_404(Coupon, code=code)
        order.coupon = coupon
        order.save()
        return Response(status=HTTP_200_OK)


class CountryListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(countries, status=HTTP_200_OK)


class AddressList(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request,format=None):
        user_id = request.user.id
        addresses = Address.objects.filter(user_id=user_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request,format=None):
        request.data["user_id"] = request.user.id
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressDetail(APIView):
    permission_classes = (IsAuthenticated, )
    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        permission_classes = (IsAuthenticated, )
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class CategoryList(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAuthenticated, )
        categories = Category.objects.filter(display=True).filter(parent__isnull=True).order_by('order')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class CategoryDetail(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs.get('slug'))
        all_cats = category.get_all_children()
        category_ids = Category.objects.filter(all_cats).values_list("id", flat=True)

        items = Item.objects.filter(category__id__in=category_ids)
        if self.request.GET.get("filters"):
            item_ids = items.values_list('id', flat=True)
            filters = self.request.GET.getlist("filters")
            for item in filters:
                values = item.split(",")
                new_ids = ItemOption.objects.filter(value__in=values).values_list('item_id', flat=True)
                item_ids = list(set(item_ids) & set(new_ids))
            return items.filter(pk__in=item_ids)
            print(item_ids)
        return items


class BrandDetail(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs.get('slug'))

        items = Item.objects.filter(brand_id=brand.id)
        if self.request.GET.get("filters"):
            item_ids = items.values_list('id', flat=True)
            filters = self.request.GET.getlist("filters")
            for item in filters:
                values = item.split(",")
                new_ids = ItemOption.objects.filter(value__in=values).values_list('item_id', flat=True)
                item_ids = list(set(item_ids) & set(new_ids))
            return items.filter(pk__in=item_ids)
            print(item_ids)
        return items

# class CategoryDetail(APIView):
#     serializer_class = ItemSerializer
#     pagination_class = StandardResultsSetPagination
#
#     @property
#     def paginator(self):
#         if not hasattr(self, '_paginator'):
#             if self.pagination_class is None:
#                 self._paginator = None
#             else:
#                 self._paginator = self.pagination_class()
#         else:
#             pass
#         return self._paginator
#     def paginate_queryset(self, queryset):
#
#         if self.paginator is None:
#             return None
#         return self.paginator.paginate_queryset(queryset,
#                    self.request, view=self)
#     def get_paginated_response(self, data):
#         assert self.paginator is not None
#         return self.paginator.get_paginated_response(data)
#
#
#     def post(self, request, slug, format=None):
#         items = Item.objects.filter(category__slug=self.kwargs.get('slug'))
#         print(request.data['filters'])
#         res = self.paginate_queryset(items)
#         if res is not None:
#             serializer = self.get_paginated_response(self.serializer_class(res,
#  many=True).data)
#         else:
#             serializer = self.serializer_class(items, many=True)
#         return Response(serializer.data, status=HTTP_200_OK)

class CategoryFilters(APIView):
    def get(self, request, slug, format=None):
        category = Category.objects.get(slug=slug)
        all_cats = category.get_all_children()
        category_ids = Category.objects.filter(all_cats).values_list("id", flat=True)
        items = Item.objects.filter(category_id__in = category_ids)
        options = {}
        values = []
        keys = []
        for item in items:
            itemoptions = ItemOption.objects.filter(item_id = item.id)
            for opt in itemoptions:
                if opt.option is not None and opt.option not in options.keys():
                    options[str(opt.option)] = [opt.value]
                elif opt.option is not None and opt.value not in options[str(opt.option)]:
                    options[str(opt.option)].append(opt.value)


        for k , v in options.items():
            values.append({"key": k, "values": v})
        return JsonResponse({"filters": values}, safe=False, status=HTTP_200_OK)





class BrandList(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAuthenticated, )
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandDetail(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self,  *args, **kwargs):
        return Item.objects.filter(brand__slug=self.kwargs.get('slug'))


class Search(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination
    def get_queryset(self,  *args, **kwargs):
        items =  Item.objects.filter(name__contains=self.request.query_params.get('keyword', ''))
        if 'slug' in self.request.query_params:
            items = items.filter(category__slug=self.request.query_params.get('slug', ''))
        return items


class KeywordSearch(ListAPIView):
    serializer_class = ItemSerializer
    def get_queryset(self,  *args, **kwargs):
        items =  Item.objects.filter(name__contains=self.request.query_params.get('keyword', ''))
        if 'slug' in self.request.query_params:
            items = items.filter(category__slug=self.request.query_params.get('slug', ''))
        return items[:int(self.request.query_params.get('limit', 10))]

class WishlistToggle(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, slug, format=None):
        user_id = request.user.id

        w = Wishlist.objects.filter(item__slug=slug).filter(user_id=user_id)
        if w:
            w.delete()
            return Response({'wishlist': False}, status=HTTP_200_OK)
        w = Wishlist()
        item = Item.objects.get(slug=slug)
        w.item_id = item.id
        w.user_id = user_id
        w.save()
        return Response({'wishlist': True}, status=HTTP_200_OK)



class ItemSpecList(APIView):
    def get(self, request, slug, format=None):
        product = Item.objects.get(slug=slug)

        serializer = ItemSpecSerializer(product.specs, many=True)
        return Response(serializer.data)

class SliderList(APIView):
    def get(self, request, format=None):
        sliders = Slider.objects.filter(display=True)
        now=datetime.date.today()
        # sliders = sliders.filter(finish_date__lte=now)
        sliders = sliders.order_by('order')
        serializer = SliderSerializer(sliders, many=True)
        return Response(serializer.data)


class HomeList(APIView):
    def get(self, request, format=None):

        categories = Category.objects.filter(display=True).filter(parent__isnull=True)
        articles = Article.objects.all().order_by('-created_at')[0:10]
        brands = Brand.objects.all()
        sliders = Slider.objects.all()
        return JsonResponse({
            "latest_products": SingleCategoryAndProductSerializer(categories, many=True).data,
            "latest_articles": ArticleSerializer(articles, many=True).data,
            "brands": BrandSerializer(brands, many=True).data,
            "sliders": SliderSerializer(sliders, many=True).data,
        })


class SameCategory(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, format=None):
        flag = True
        data = request.data
        ids = data["product_ids"]
        first_item = Item.objects.get(pk=ids[0])
        for id in ids:
            temp = Item.objects.get(pk=id)
            if temp.category_id != first_item.category_id:
                flag = False 
                break
        return Response({ "result": flag },status=HTTP_200_OK)


class CompareList(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, format=None):
        data = request.data
        ids = data["product_ids"]
        items = Item.objects.filter(pk__in=ids)
        serializer = CompareListSerializer(items, many=True)
        return Response(serializer.data)


class ArticleList(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        items = Article.objects.all().order_by('-created_at')
        serializer = ArticleSerializer(items, many=True)
        return Response(serializer.data)

class ArticleDetail(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request, slug, format=None):
        try:
            item = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        serializer = ArticleSerializer(item)
        return Response(serializer.data)


class PageList(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        items = Page.objects.all()
        serializer = PageSerializer(items, many=True)
        return Response(serializer.data)

class PageDetail(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request, slug, format=None):
        try:
            item = Page.objects.get(slug=slug)
        except Page.DoesNotExist:
            raise Http404
        serializer = PageSerializer(item)
        return Response(serializer.data)


class MenuList(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        menu = Menu.objects.filter(display=True).order_by('order')
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data)

class CompareList(APIView):
    def post(self, request, *args, **kwargs):
        ids = request.data.get('item_ids', [])
        print(ids)
        res = True
        if len(ids) == 1:
            res = True
        elif len(ids) > 1:
            first_item = Item.objects.get(pk=ids[0])
            last_item = Item.objects.get(pk=ids[-1])

            if first_item.category_id != last_item.category_id:
                res = False
        else:
            res = False 
        return Response(data = res, status=HTTP_200_OK)

class CompareListItems(APIView):
    def post(self, request, *args, **kwargs):
        ids = request.data.get('item_ids', None)
        items = Item.objects.filter(pk__in=ids)
        serializer = SingleItemSerializer(items, many=True)
        return Response(serializer.data)