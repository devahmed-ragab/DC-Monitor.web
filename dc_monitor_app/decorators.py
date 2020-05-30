from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    """
     Prevent user from going to parameter function while he is authenticated
    :param view_func
    :return 'user_dashboard' if 'authenticated' else 'view_func'
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard_view')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_groups(groups=[]):
    """
    :param groups:
    :return view_func if 'user_group' in 'groups' else 'you are not allowed'
    """

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in groups:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('YOU ARE NOT Allowed')
        return wrapper_func

    return decorator


def admin_only(view_func):
    """
    Allow only 'request.user.groups' with super_admin group, if not redirect
    to 'user_dashboard'
    :param view_func
    :return view_func if group = 'superadmin' else 'user_dashboard'
    """

    def wrapper_func(request, *args, **kwargs):
        # if request.user.groups.exists():
        #     group = request.user.groups.all()[0].name
        #     if group == 'super_admin':
        #         return view_func
        #     else:
        #         return redirect('user_dashboard')
        # return view_func
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'superadmin':
            return view_func(request, *args, **kwargs)
        if group == 'user':
            return redirect('user_dashboard')
        else:
            return HttpResponse('not superadmin or user ')

    return wrapper_func
