from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def sign_up(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username=email, email=email, password=password, first_name=fname, last_name=lname)
        login(request, authenticate(request, username=email, password=password))
        return redirect("index")
    else:
        pass
    return render(request,'registration/register.html')
    
def log_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else: 
                pass
        else: 
            print(user, email, password)
            return render(request,'registration/login.html')
    else:
        pass
    return render(request,'registration/login.html')

@login_required
def log_out(request):
    logout(request)
    return redirect("index")


@login_required
def add_recipe(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username=email, email=email, password=password, first_name=fname, last_name=lname)
        login(request, authenticate(request, username=email, password=password))
        return redirect("index")
    else:
        pass
    return render(request,'recipe/add_recipe.html')