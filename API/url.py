from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url, include
from rest_framework.authtoken import views as rest_views
from django.urls import path
from API import views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('smartmeter', views.SmartMeterView)
router.register('Clint', views.ClintSerializerView)
router.register('user', views.UserSerializerView)
router.register('Bill', views.BillSerializerView)
router.register('ApplianceCategory', views.ApplianceCategorySerializerView)
router.register('Seller', views.SellerSerializerView)
router.register('Appliances', views.AppliancesSerializerView)

urlpatterns = [
    # get user token takes post request with username and password
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('', include(router.urls)),
    path('login', rest_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
