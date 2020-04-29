from django.urls import path
from .views import *

urlpatterns = [
    # path('dashboard/<str:pk>', dashboard_view, name='dashboard_view'),
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('login/', login_view, name='login_view'),
    path('registration/', registration_view, name='registration_view'),
    path('logout/', logout_view, name='logout'),
    path('user/', user_dashboard_view, name='user_dashboard'),
    path('add-device/', add_smartmeter_view, name='add_device')
]