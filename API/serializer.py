from abc import ABC

from django.forms import FileField
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    CharField,
    IntegerField,
    EmailField,
    ImageField
)
from rest_framework.validators import UniqueValidator

from dc_monitor_app.models import (
    SmartMeters,
    Clint,
    Bill,
    ApplianceCategory,
    Seller,
    Factory,
    Appliances
)


class ClintSerializer(ModelSerializer):
    class Meta:
        model = Clint
        fields = ['location', 'date_created', 'phone_number', 'prof_image']

        extra_kwargs = {
            "prof_image": {
                "read_only": False,

            }
        }


class ImageSerializer(ModelSerializer):
    prof_image = ImageField()

    class Meta:
        model = Clint
        fields = ['prof_image']


class UserClintValidatedSerializer(ModelSerializer):
    clint = ClintSerializer(many=False, read_only=True)
    email = EmailField(label='Email')
    first_name = CharField()
    last_name = CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'clint']

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs:
            raise ValidationError('This email has already registered.')
        return data

    def create(self, validated_data):
        print(validated_data)
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']

        user_obj = User(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        print(f'{username} has been created !')
        return user_obj
    #
    # def update(self, instance, validated_data):
    #     instance.paassword = validated_data.get('username', instance.password)
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.update
    #     return instance


class SmartMeterSerializer(ModelSerializer):
    SER = CharField(required=False,
                    validators=[
                        RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')
                    ])

    class Meta:
        model = SmartMeters
        fields = ['SER', 'consumption', 'device_status', 'conception_cost']


class UserProfileSerializer(ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This Email already Exist")
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        extra_kwargs = {
            "password": {
                "requirement": False,
                'blank': True
            }
        }


class SERSerializer(ModelSerializer):
    class Meta:
        model = SmartMeters
        fields = ['SER', 'user']


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        fields = ['user', 'consumption', 'bill', 'price_category', 'conception_date']


class WattageCalculator(serializers.Serializer):
    wattage = serializers.FloatField(required=True)
    hours = serializers.FloatField(required=True)
    days = serializers.IntegerField(required=True)


class ApplianceCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ApplianceCategory
        fields = '__all__'


class SellerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class AppliancesSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Appliances
        fields = '__all__'
