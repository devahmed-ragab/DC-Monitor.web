from django.urls import path
from .views import *

urlpatterns = [
    # path('dashboard/<str:pk>', dashboard_view, name='dashboard_view'),
    path('login/', login_view, name='login_view'),
    path('registration/', registration_view, name='registration_view'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/', dashboard_view, name='dashboard_view'),

    path('add-device/', add_smartmeter_view, name='add_device'),
    path('edit-device/<str:SER>/', edit_tool, name='edit_tool'),
    path('delete-device/<str:SER>/', delete_tool, name='delete_tool'),
    path('all-devices/', all_devices_view, name='all_device'),

    path('add_appliance/', add_appliance_view, name='add_appliance_view'),
    path('all_appliance/', all_appliance_view, name='all_appliance_view'),
    path('edit_appliance/<str:id>/', edit_appliance_view, name='edit_appliance_view'),

    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
    path('all-customers-form/', all_customers_view, name='all_customers_view'),

    path('user/', user_dashboard_view, name='user_dashboard'),
]
