
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url, include
from rest_framework.authtoken import views as rest_views
from django.urls import path
from API import views
from rest_framework import routers, renderers
from .views import *


router = routers.DefaultRouter()
router.register('smartmeter', views.SmartMeterView)
router.register('Seller', views.SellerSerializerView)
router.register('Seller', views.SellerSerializerView)
router.register('Appliances', views.AppliancesSerializerView)
router.register('ApplianceCategory', views.ApplianceCategorySerializerView)



urlpatterns = [
    # get user token takes post request with username and password
    path('token/auth', CustomAuthToken.as_view()),
    path('register', UserCreateAPIView.as_view(), name='register'),
    path('bill', BillAPIView.as_view(), name='api_bill'),
    path('user/profile', UserDetailView.as_view()),
    path('user/image', UserImageDetailView.as_view()),



    path('', include(router.urls))


]
