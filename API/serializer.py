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


class ClintSerializer(ModelSerializer):
    class Meta:
        model = Clint
        fields = [ 'location', 'date_created', 'phone_number', 'prof_image']


class UserSerializer(ModelSerializer):
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
    clint = ClintSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'clint']

        extra_kwargs = {
            "password": {
                "requirement": False,
                'blank': True
            }
        }



class PasswordSerializer(ModelSerializer):
    password = CharField(required=True, write_only=True)


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        fields = ['user', 'consumption', 'bill', 'price_category', 'conception_date']


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
