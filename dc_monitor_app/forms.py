from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.forms import ModelForm, Select
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


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
        # widgets = {
        #     'seller': Select(),
        # }
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
