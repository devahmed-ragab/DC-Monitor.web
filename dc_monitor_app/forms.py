from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.forms import ModelForm,  Select
from .models import *


class CreateClintForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddDeviceForm(ModelForm):
    SER = models.CharField(
        validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')])

    class Meta:
        model = SmartMeters
        fields = ['SER']


class AddApplianceForm(ModelForm):
    class Meta:
        model = Appliances
        widgets = {
            'seller': Select(),
        }
        fields = ['appliance_category', 'consumption_label', 'model', 'name',
                  'wattage', 'factory', 'price', 'seller', 'sub_category','warranty']
