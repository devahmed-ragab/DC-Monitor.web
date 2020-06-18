from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    CharField,
    EmailField,
)
from dc_monitor_app.models import (
    SmartMeters,
    Clint,
    Bill,
    ApplianceCategory,
    Seller,
    Factory,
    Appliances
)


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email')
    first_name = CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs:
            raise ValidationError('This user has already registered.')
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


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        return data


class SmartMeterSerializer(HyperlinkedModelSerializer):
    SER = CharField(required=False,
                    validators=[
                        RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')
                    ])

    class Meta:
        model = SmartMeters
        fields = ['user', 'SER', 'consumption', 'device_status']


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class ClintSerializer(HyperlinkedModelSerializer):
    user = UserSerializer

    class Meta:
        model = Clint
        fields = ['user', 'location', 'date_created', 'phone_number', 'prof_image']


class BillSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


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
