from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from API.serializer import (
    ApplianceCategorySerializer,
    SmartMeterSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    ClintSerializer,
    BillSerializer,
    SellerSerializer,
    AppliancesSerializer,
    UserSerializer

)
from dc_monitor_app.models import *


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_class = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SmartMeterView(viewsets.ModelViewSet):
    queryset = SmartMeters.objects.all()
    serializer_class = SmartMeterSerializer


class ClintSerializerView(viewsets.ModelViewSet):
    queryset = Clint.objects.all()
    serializer_class = ClintSerializer


class UserSerializerView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BillSerializerView(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class ApplianceCategorySerializerView(viewsets.ModelViewSet):
    queryset = ApplianceCategory.objects.all()
    serializer_class = ApplianceCategorySerializer


class SellerSerializerView(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class AppliancesSerializerView(viewsets.ModelViewSet):
    queryset = Appliances.objects.all()
    serializer_class = AppliancesSerializer
