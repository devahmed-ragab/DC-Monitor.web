from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.forms import ModelForm, Select
from django import forms

from .models import *


class CreateUserForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField()
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs:
            print("This email has already registered")
            raise forms.ValidationError('This email has already registered.')
        return email

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError('user name is too short it must be more than 3 characters.')

        # user_qs = User.objects.filter(email=email)
        # if user_qs:
        #     raise forms.ValidationError('This email has already registered.')
        return username


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class AddDeviceForm(ModelForm):
    SER = models.CharField(
        validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')])

    class Meta:
        model = SmartMeters
        fields = ['SER']


class AddApplianceForm(ModelForm):
    class Meta:
        model = Appliances
        fields = ['appliance_category', 'consumption_label', 'model', 'name',
                  'wattage', 'factory', 'price', 'seller', 'sub_category', 'warranty']


class CreateClintForm(ModelForm):
    class Meta:
        model = Clint
        fields = ['prof_image', 'location', 'phone_number']


class EditCustomerUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']


class EditCustomerPhoneForm(ModelForm):
    class Meta:
        model = Clint
        fields = ['phone_number']


class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        """
        Cleaning email field
        """
        email = self.cleaned_data.get('email', None)

        if email:
            try:
                email = User.objects.get(email=email)
            except email.DoesNotExist():
                raise forms.ValidationError('This email does not exist.')
        return email


class DeviceFormValidation(ModelForm):
    SER = models.CharField(
        validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')])

    class Meta:
        model = SmartMeters
        fields = ['SER', 'user']

    def clean_SER(self):
        SER = self.cleaned_data.get('SER')

        try:
            SER = SmartMeters.objects.get(SER=SER)
        except SmartMeters.DoesNotExist():
            raise ValidationError('This Smart Meter does not exist.')
            print("This Smart Meter does not exist")
        if SER.user:
            raise ValidationError('This Smart Meter already registered.')
            print("This Smart Meter already registered")
        return SER
