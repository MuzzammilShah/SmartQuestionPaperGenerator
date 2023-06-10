from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Not authorized to view this page")
        return wrapper_func
    return decorator


def allowed_dept(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0]

        if str(group.name)=='Admin':
            return view_func(request, pk, *args, **kwargs)
        
        elif str(group.id)==str(pk):
            return view_func(request, pk, *args, **kwargs)  
        else:
            return HttpResponse("Not authorized to view this page")
    return wrapper_func

def allowed_course(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0]

        if str(group.name)=='Admin':
            return view_func(request, pk, *args, **kwargs)
        
        elif str(group.id)==str(Course.objects.get(id=pk).dept.id):
            return view_func(request, pk, *args, **kwargs)  
        else:
            return HttpResponse("Not authorized to view this page")
    return wrapper_func

def allowed_module(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0]

        if str(group.name)=='Admin':
            return view_func(request, pk, *args, **kwargs)
        
        elif str(group.id)==str(Module.objects.get(id=pk).course.dept.id):
            return view_func(request, pk, *args, **kwargs)  
        else:
            return HttpResponse("Not authorized to view this page")
    return wrapper_func

def allowed_mcq(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0]

        if str(group.name)=='Admin':
            return view_func(request, pk, *args, **kwargs)
        
        elif str(group.id)==str(Mcq.objects.get(id=pk).module.course.dept.id):
            return view_func(request, pk, *args, **kwargs)  
        else:
            return HttpResponse("Not authorized to view this page")
    return wrapper_func

def allowed_question(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        print(Question.objects.get(id=pk).module.course.dept.id)
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0]

        if str(group.name)=='Admin':
            return view_func(request, pk, *args, **kwargs)
        
        elif str(group.id)==str(Question.objects.get(id=pk).module.course.dept.id):
            return view_func(request, pk, *args, **kwargs)  
        else:
            return HttpResponse("Not authorized to view this page")
    return wrapper_func