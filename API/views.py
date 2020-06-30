
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, status, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, permission_classes
from rest_framework.settings import api_settings
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from API.serializer import (
    ApplianceCategorySerializer,
    SmartMeterSerializer,
    UserSerializer,
    # UserLoginSerializer,
    ClintSerializer,
    BillSerializer,
    SellerSerializer,
    AppliancesSerializer,
    UserSerializer,
    UserProfileSerializer,
    PasswordSerializer)
from dc_monitor_app.models import *


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'user': user_serializer.data,
        })


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

#
# class UserUpdateAPIView(APIView):
#
#     def post(self, request, format=None):
#         user = request.user
#         user_serializer = UserProfileSerializer(user, request.data)
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return Response(user_serializer.data, self=status.HTTP_200_OK)
#         return Response(user_serializer.errors)

#
# class UserUpdateAPIView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserProfileSerializer


class BillAPIView(APIView):

    def get(self, request, format=None):

        clint = request.user.clint

        try:
            clint_bill = clint.bill_set.order_by('-conception_date')[0]

        except IndexError:
            return Response("no bills for this user.", status=status.HTTP_204_NO_CONTENT)

        meters = clint.smartmeters_set.all()

        bill_serializer = BillSerializer(clint_bill)
        meter_serializer = SmartMeterSerializer(meters, many=True)

        return Response({
            'bill': bill_serializer.data,
            'smartmeters': meter_serializer.data
        }, status=status.HTTP_200_OK)


# class UserDetailView(APIView):

    # def get(self, request, format=None):
    #     user = request.user
    #     serializer = UserProfileSerializer(user)
    #     return Response(serializer.data)

    # @permission_classes((AllowAny,))
    # def post(self, request, format=None):
    #     user_serializer = UserSerializer(request.data)
    #     if user_serializer.is_valid():
    #         user_serializer.save()
    #         return Response(user_serializer.data, self=status.HTTP_200_OK)
    #     return Response(user_serializer.errors)

    # def post(self, request, format=None):
    #     try:
    #         user = User.objects.get(id=request.user.id)
    #     except User.DoesNotExist:
    #         return Response(data='no such user!', status=status.HTTP_400_BAD_REQUEST)
    #     profile_user = Clint.objects.filter(user=request.user)
    #     clint_serializer = ClintSerializer(profile_user)
    #     user_serializer = UserProfileSerializer(user, data=request.data)
    #
    #     if user_serializer.is_valid() and clint_serializer.is_valid():
    #         user_serializer.save()
    #         clint_serializer.save()
    #         return Response(user_serializer.data, self=status.HTTP_200_OK)
    #     return Response(user_serializer.errors)
    #
    # def delete(self, request, pk, format=None):
    #     user = request.user
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class SmartMeterView(viewsets.ModelViewSet):
    queryset = SmartMeters.objects.all()
    serializer_class = SmartMeterSerializer


class ClintSerializerView(viewsets.ModelViewSet):
    queryset = Clint.objects.all()
    serializer_class = ClintSerializer


class UserSerializerView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApplianceCategorySerializerView(viewsets.ModelViewSet):
    queryset = ApplianceCategory.objects.all()
    serializer_class = ApplianceCategorySerializer


class SellerSerializerView(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class AppliancesSerializerView(viewsets.ModelViewSet):
    queryset = Appliances.objects.all()
    serializer_class = AppliancesSerializer
