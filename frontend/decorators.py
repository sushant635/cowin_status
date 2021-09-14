from django.http import HttpResponse
from django.shortcuts import redirect
# import datetime
from datetime import datetime,timedelta

def type_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.get().name
            print(group)
        if group == 'employee':
            return redirect('user_profile')
        else:
            return redirect('dashboard')
            # return view_func(request,*args,**kwargs)

        # if request.user.is_authenticated:
        #     return redirect('dashboard')

        # else:
        #     return view_func(request,*args,**kwargs)

    return wrapper_func


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.get()
            print(group)
        if request.user.is_authenticated:
            return redirect('dashboard')

        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func

def employee_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'employee':
            print('working')
            return view_func(request,*args,**kwargs)
    return wrapper_func