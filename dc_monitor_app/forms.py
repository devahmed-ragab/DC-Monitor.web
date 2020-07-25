
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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

    def clean_SER(self):
        # validation on the form level it dosn't do it on the modle
        SER = self.cleaned_data.get('SER')
        if SER.count == 1234567890:
            raise forms.ValidationError("1234567890 not allowed")
        return SER


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
