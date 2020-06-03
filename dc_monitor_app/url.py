from django.urls import path
from .views import *

urlpatterns = [
    # path('dashboard/<str:pk>', dashboard_view, name='dashboard_view'),
    path('', dashboard_view, name='dashboard_view'),
    path('login/', login_view, name='login_view'),
    path('registration/', registration_view, name='registration_view'),
    path('logout/', logout_view, name='logout'),

    path('devices/', all_meters_view, name='all_meters'),
    path('devices/add', add_meter_view, name='add_meter'),
    path('devices/<str:SER>/', edit_meter, name='edit_meter'),
    path('devices/<str:SER>/delete', delete_meter, name='delete_meter'),

    path('customers/', all_customers_view, name='all_customers_view'),
    path('customers/<str:id>/delete', delete_customers_view, name='delete_customer'),
    path('customers/<str:id>/edit', edit_customers_view, name='edit_customer'),

    path('add_appliance/', add_appliance_view, name='add_appliance_view'),
    path('all_appliance/', all_appliance_view, name='all_appliance_view'),
    path('delete_appliance/<str:id>', delete_appliance_view, name='delete_appliance'),
    path('edit_appliance/<str:id>/', edit_appliance_view, name='edit_appliance_view'),

    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),


    path('user/', user_dashboard_view, name='user_dashboard'),
]
