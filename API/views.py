from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, status, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.settings import api_settings
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from API.serializer import (
    ApplianceCategorySerializer,
    SmartMeterSerializer,
    UserClintValidatedSerializer,
    # UserLoginSerializer,
    ClintSerializer,
    BillSerializer,
    SellerSerializer,
    AppliancesSerializer,
    UserClintValidatedSerializer,
    UserProfileSerializer,
    PasswordSerializer, ImageSerializer, SERSerializer)
from dc_monitor_app.models import *


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserClintValidatedSerializer(user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'user': user_serializer.data,
        })


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserClintValidatedSerializer
    queryset = User.objects.all()


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


class UserDetailView(APIView):
    parser_class = (FormParser, MultiPartParser, JSONParser, FileUploadParser)

    def get(self, request, format=None):
        user = request.user
        serializer = UserClintValidatedSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = request.user

        user_serializer = UserProfileSerializer(user, data=request.data)
        clint_serializer = ClintSerializer(user.clint, data=request.data)

        if user_serializer.is_valid() and clint_serializer.is_valid():
            user_serializer.save()
            clint_serializer.save()

            return Response({'user': user_serializer.data,
                             'clint': clint_serializer.data
                             }, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserImageDetailView(APIView):
    parser_class = (FormParser, MultiPartParser, JSONParser)

    def get(self, request, format=None):
        user = request.user
        serializer = ImageSerializer()
        if not user.is_anonymous:
            clint = user.clint
            serializer = ImageSerializer(clint)
        return Response(serializer.data)

    def put(self, request):
        user = request.user.clint
        print(user)
        serializer = ImageSerializer(user, data=request.data)
        if serializer.is_valid():
            print("valid : Image Uploaded successfully ")
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class UserAddSER(APIView):

    def put(self, request):
        user = request.user.clint
        SER = request.data['SER']
        try:
            smartmeter_qs = SmartMeters.objects.get(SER=SER)
        except SmartMeters.DoesNotExist:
            raise ValidationError('This SER dose not exist.')

        if smartmeter_qs.user:
            raise ValidationError('This SER dose has a user.')

        serializer = SERSerializer(smartmeter_qs, data=request.data)
        if serializer.is_valid():
            print("valid : SER Uploaded successfully ")
            smartmeter_qs.user
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class SmartMeterView(viewsets.ModelViewSet):
    queryset = SmartMeters.objects.all()
    serializer_class = SmartMeterSerializer


class UserSerializerView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserClintValidatedSerializer


class ApplianceCategorySerializerView(viewsets.ModelViewSet):
    queryset = ApplianceCategory.objects.all()
    serializer_class = ApplianceCategorySerializer


class SellerSerializerView(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class AppliancesSerializerView(viewsets.ModelViewSet):
    queryset = Appliances.objects.all()
    serializer_class = AppliancesSerializer
