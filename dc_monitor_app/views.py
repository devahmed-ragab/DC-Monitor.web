from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from dc_monitor_app.models import Clint, SmartMeters
from .forms import CreateClintForm
from django.contrib import messages
from .decorators import *

from datetime import date, timedelta


def percentage(on_devices, all_devices):
    try:
        div_sum = on_devices / all_devices
    except ZeroDivisionError:
        div_sum = 0

    on_devic_percentage = div_sum * 100
    return on_devic_percentage


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        print("Posting data ...", request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        clint = authenticate(request, username=username, password=password)
        print("login clint = ", clint)
        if clint is not None:
            login(request, clint)
            return redirect(dashboard_view)
        else:
            messages.info(request, 'username or password is wrong')

    return render(request, 'dc_monitor_app/login_page.html')


@unauthenticated_user
def registration_view(request):
    form = CreateClintForm()
    if request.method == 'POST':
        form = CreateClintForm(request.POST)
        if form.is_valid():
            print(" request valid :")
            registration_user = form.save()
            user_name = form.cleaned_data.get('username')

            group = Group.objects.get(name='user')
            registration_user.groups.add(group)

            Clint.objects.create(
                user=registration_user,
                first_name=form.cleaned_data.get('first_name')
            )

            messages.success(request, 'Account successfully created ' + user_name)
            return redirect('login_view')

    context = {"form": form}
    return render(request, 'dc_monitor_app/registration_page.html', context)


@allowed_groups(groups=['user', 'superadmin'])
def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required(login_url='login_view')
@admin_only
def dashboard_view(request):
    devices = SmartMeters.objects.all()
    devices_num = devices.count()
    working_devices = (devices.filter(device_status=1).count() / devices_num) * 100 if devices_num > 0 else 0

    days_before_30 = (date.today() - timedelta(days=30)).isoformat()

    users = Clint.objects.all()
    users_count = users.count()
    new_customers = users.filter(date_created__gte=days_before_30).count()
    new_customers_percentage = (new_customers / users_count) * 100 if users_count > 0 else 0

    # active_users = users.filter(is_active=True).count()
    # active_users_percentage = (active_users / users_count) * 100

    context = {
        'users_count': users_count,
        'devices_num': devices_num,
        'new_customers_count': new_customers,
        'working_devices': working_devices,
        'new_customers_percentage': new_customers_percentage
    }
    print(context)

    return render(request, 'dc_monitor_app/dashboard.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['user'])
def user_dashboard_view(request):
    devices = request.user.clint.smartmeters_set
    working_dev = devices.filter(device_status=1).count()
    on_dev_percentage = percentage(working_dev, devices.count())
    context = {
        'devices': devices,
        'working_dev': working_dev,
        'dev_percentage': on_dev_percentage,
    }
    return render(request, 'dc_monitor_app/user_page.html', context)


@allowed_groups(groups=['superadmin'])
def add_smartmeter_view(request):
    context = {
    }
    return render(request, 'dc_monitor_app/add_tool_page.html', context)
