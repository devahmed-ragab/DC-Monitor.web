from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response

from .decorators import *
from .forms import *
from .models import Clint


def percentage(on_devices, all_devices):
    try:
        div_sum = on_devices / all_devices
    except ZeroDivisionError:
        div_sum = 0

    on_devi_percentage = div_sum * 100
    return int(on_devi_percentage)


@unauthenticated_user
def login_view(request):
    print("login view !")
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

    return render(request, 'dc_monitor_app/registraion/login_page.html')


@unauthenticated_user
def registration_view(request):
    form_r = CreateUserForm()
    if request.method == 'POST':
        form_r = CreateUserForm(request.POST)
        terms = request.POST.get('check')
        print("POST registr")
        if form_r.is_valid() and terms:
            print(" request valid :")
            form_r.save()
            user_name = form_r.cleaned_data.get('username')
            messages.success(request, 'Account successfully created ' + user_name)
            return render(request, 'dc_monitor_app/registraion/email-verify.html')

    context = {"form": form_r}
    return render(request, 'dc_monitor_app/registraion/registration_page.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['user', 'superadmin'])
def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required(login_url='login_view')
@admin_only
def dashboard_view(request):
    devices = SmartMeters.objects.all()
    devices_num = devices.count()
    working_devices = percentage(devices.filter(device_status=1).count(), devices_num)
    days_before_30 = (date.today() - timedelta(days=30)).isoformat()

    users = Clint.objects.all()
    users_count = users.count()
    new_customers = users.filter(date_created__gte=days_before_30).count()
    new_customers_percentage = percentage(new_customers, users_count)

    context = {
        'users_count': users_count,
        'devices_num': devices_num,
        'new_customers_count': new_customers,
        'working_devices': working_devices,
        'new_customers_percentage': new_customers_percentage
    }
    return render(request, 'dc_monitor_app/admin/dashboard.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['user'])
def user_dashboard_view(request):
    clint = request.user.clint
    devices = clint.smartmeters_set
    working_dev = devices.filter(device_status=1)
    on_dev_percentage = percentage(working_dev.count(), devices.count())

    try:
        clint_bill = clint.bill_set.order_by('-conception_date')[0]
    except IndexError:
        clint_bill = 0

    context = {
        'devices': devices,
        'working_dev': working_dev,
        'user_bill': clint_bill,
        'dev_percentage': on_dev_percentage,
    }
    return render(request, 'dc_monitor_app/user/user_page.html', context)


def user_dashboard_ajax(request):
    print("user_dashboard_ajax:")
    if request.is_ajax and request.method == "GET":

        clint = request.user.clint
        devices = clint.smartmeters_set
        working_dev = devices.filter(device_status=1)
        on_dev_percentage = percentage(working_dev.count(), devices.count())

        try:
            clint_bill = clint.bill_set.order_by('-conception_date')[0]
        except IndexError:
            clint_bill = 0
        user_bill = clint_bill.consumption
        return Response({
            'devices': devices,
            'working_dev': working_dev,
            'user_bill': user_bill
            # 'dev_percentage': on_dev_percentage,
        }, status=status.HTTP_200_OK)


# meter
@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def add_meter_view(request):
    form = AddDeviceForm()
    if request.method == 'POST':
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            print('valid SER ')
            form.save()
    context = {
        'form': form
    }
    return render(request, 'dc_monitor_app/admin/add_tool_page.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin', 'user'])
def all_meters_view(request):
    if request.user.groups.get() == 'user':
        return redirect('configuration')
    devices = SmartMeters.objects.all()
    context = {
        'devices': devices
    }
    return render(request, 'dc_monitor_app/admin/all_tools_page.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def edit_meter(request, SER):
    # todo add user edite tool
    print("editing tool")
    tool = SmartMeters.objects.get(SER=SER)
    form = AddDeviceForm(instance=tool)
    if request.method == 'POST':
        print("post data >> ", request.POST)
        form = AddDeviceForm(request.POST, instance=tool)
        if form.is_valid():
            form.save()
            print("SER updated")
            return redirect('all_meters')
        else:
            messages.error(request, 'SER is not valid')
    context = {
        'form': form
    }
    return render(request, 'dc_monitor_app/admin/edit_tool.html', context)


# customer
@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def all_customers_view(request):
    # group = Group.objects.get(name='user')
    # users = group.user_set.all()
    users = User.objects.filter(groups__name='user')
    print(f"all users : {users}")
    context = {
        'users': users
    }
    return render(request, 'dc_monitor_app/user/customer_form_page.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def delete_customers_view(request, id):
    customer = Clint.objects.get(id=id)
    user = customer.user
    if request.method == 'POST':
        user.delete()
        print('customer has been deleted successfully.')
        return redirect('all_customers_view')
    context = {'item': customer}
    print(f"Customers  data : {customer}")
    return render(request, 'dc_monitor_app/admin/delet_item.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def edit_customers_view(request, id):
    customer = get_object_or_404(Clint, id=id)
    devices = customer.smartmeters_set.first()
    user = customer.user

    phone_form = EditCustomerPhoneForm(instance=customer)
    user_form = EditCustomerUserForm(instance=user)
    device_form = AddDeviceForm(instance=devices)

    if request.method == 'POST':
        phone_form = EditCustomerPhoneForm(request.POST, instance=customer)
        user_form = EditCustomerUserForm(request.POST, instance=user)
        device_form = AddDeviceForm(request.POST, instance=devices)
        if user_form.is_valid and phone_form.is_valid and device_form.is_valid:
            user_form.save()
            phone_form.save()
            return redirect(all_customers_view)

    context = {
        'phone_form': phone_form,
        'user_form': user_form,
        'device_form': device_form,
        'user': user
    }
    return render(request, 'dc_monitor_app/admin/eedit_customer_page.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def all_appliance_view(request):
    appliance = Appliances.objects.all()
    context = {
        'appliance': appliance
    }
    return render(request, 'dc_monitor_app/admin/all_appliance_page.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def add_appliance_view(request):
    print("add appliancee ..... ")
    form = AddApplianceForm()
    if request.method == "POST":
        print("posting data .. ")
        form = AddApplianceForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("saving form ....")
            form.save()
            messages.success(request, 'New Appliance has been added successfully.')
            form = AddApplianceForm()
    context = {
        'form': form
    }
    return render(request, 'dc_monitor_app/admin/add_appliance_page.html', context)


@login_required(login_url='login_view')
def edit_profile_view(request):
    # groups = request.user.groups.all()
    user = request.user
    clint = user.clint
    groups = user.groups.all()
    user_form = EditUserForm(instance=user)
    clint_form = CreateClintForm(instance=clint)
    if request.method == 'POST':
        print(f"posting data   clint {request.method}")
        user_form = EditUserForm(request.POST, instance=user)
        clint_form = CreateClintForm(request.POST, request.FILES, instance=clint)
        if user_form.is_valid() and clint_form.is_valid():
            print('user and clint has been saved')
            user_form.save()
            clint_form.save()
            return redirect('profile')

    context = {
        'user_form': user_form,
        'clint_form': clint_form,
        'groups': groups
    }
    print(context)

    return render(request, 'dc_monitor_app/user/edith_profile_page.html', context)


@login_required(login_url='login_view')
def profile_view(request):
    user = request.user
    devices = user.clint.smartmeters_set.all() if user.clint.smartmeters_set.all() else "Empty"
    context = {"user": user, "devices": devices}
    return render(request, 'dc_monitor_app/admin/profile_page.html', context)


@login_required(login_url='login_view')
def delete_meter(request, SER):
    device = SmartMeters.objects.get(SER=SER)
    if request.method == 'POST':
        device.delete()
        if request.user.groups.get() == 'user':
            return redirect('configuration')
        return redirect('all_meters')

    context = {
        'item': device
    }
    return render(request, 'dc_monitor_app/admin/delet_item.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['superadmin'])
def edit_appliance_view(request, id):
    print("test")
    appliance = Appliances.objects.get(id=id)
    form = AddApplianceForm(instance=appliance)
    if request.method == 'POST':
        print("post editing ", request.POST)
        form = AddApplianceForm(request.POST, instance=appliance)
        if form.is_valid():
            form.save()
            print("update")
        else:
            messages.error(request, 'updating is not valid')

    context = {
        'form': form
    }
    return render(request, 'dc_monitor_app/admin/edit_appliance.html', context)


@login_required(login_url='login_view')
def delete_appliance_view(request, id):
    device = Appliances.objects.get(id=id)
    if request.method == 'POST':
        device.delete()
        return redirect('all_appliance_view')

    context = {
        'item': device
    }
    return render(request, 'dc_monitor_app/admin/delet_item.html', context)


@login_required(login_url='login_view')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important! this keeps the user login in
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dc_monitor_app/user/change_password_page.html', {
        'form': form
    })


@login_required(login_url='login_view')
@allowed_groups(groups=['user', 'superadmin'])
def calc_wattage_view(request):
    context = {}
    return render(request, 'dc_monitor_app/user/featuers/wattage_calculation.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['user', 'superadmin'])
def advices_timeline_view(request):
    context = {}
    return render(request, 'dc_monitor_app/user/featuers/timeline.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['user', 'superadmin'])
def configuration_view(request):
    user = request.user.clint
    devices = user.smartmeters_set.all()
    context = {
        'devices': devices
    }
    return render(request, 'dc_monitor_app/user/configration.html', context)


@login_required(login_url='login_view')
@allowed_groups(groups=['user'])
def consumption_analyses(request):
    user = request.user.clint
    devices = user.smartmeters_set.all()
    context = {
        "clint": user,
        'devices': devices
    }
    return render(request, 'dc_monitor_app/user/featuers/consmption_analysis.html', context)


@unauthenticated_user
def reset_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            return render(request, 'dc_monitor_app/registraion/email-verify.html')

    context = {
    }
    return render(request, 'dc_monitor_app/registraion/forgat_password.html', context)


# meter
@login_required(login_url='login_view')
@allowed_groups(groups=['user'])
def user_meter_add(request):
    if request.method == 'POST':
        SER = request.POST.get('SER')
        user = request.user.clint
        try:
            smartmeter_qs = SmartMeters.objects.get(SER=SER)
        except SmartMeters.DoesNotExist:
            messages.error(request, 'This SER dose not exist')
            return redirect('user_meter_add')

        if smartmeter_qs.user:
            messages.error(request, 'This SER dose has a user.')
            return redirect('user_meter_add')

        smartmeter_qs.user = user
        smartmeter_qs.save()

        return redirect('configuration')

    return render(request, 'dc_monitor_app/user/featuers/user_add_meter.html')
