from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from django.forms.models import model_to_dict
from core.models import UserProfile, Order
from core.api.serializers import OrderSerializer

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_profile = UserProfile.objects.get(user__id=user.pk)
        token, created = Token.objects.get_or_create(user=user)

        order, found = Order.objects.get_or_create(
            user=user.id,
            ordered=False
        )

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'status': user_profile.status,
            'user_type': 1,
            'cart': OrderSerializer(order).data
        })