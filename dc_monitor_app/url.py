from django.urls import path
from .views import *

urlpatterns = [
    # path('dashboard/<str:pk>', dashboard_view, name='dashboard_view'),
    path('login/', login_view, name='login_view'),
    path('registration/', registration_view, name='registration_view'),
    path('logout/', logout_view, name='logout'),

    path('user/', user_dashboard_view, name='user_dashboard'),

    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('add-device/', add_smartmeter_view, name='add_device'),
    path('all-devices/', all_devices_view, name='all_device'),
    path('all-customers-form/', all_customers_view, name='all_customers_view'),
    path('add_devices/', add_appliance_view, name='add_appliance_view'),
    path('all_devices/', all_appliance_view, name='all_appliance_view')
]
