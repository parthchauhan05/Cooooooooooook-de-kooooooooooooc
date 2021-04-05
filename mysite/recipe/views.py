from mysite import settings
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Ingredient, Recipe
import datetime
# Create your views here.

def index(request):
    Recipes = Recipe.objects.all()[:3]
    template = loader.get_template('index.html')
    context = {'recipes' : Recipes}
    return render(request, 'index.html', context=context)


def sign_up(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if password == cpassword and User.object.get(email=email) :
            user = User.objects.create_user(username=email, email=email, password=password, first_name=fname, last_name=lname)
            login(request, authenticate(request, username=email, password=password))
            return redirect("index")
        else:
            context = {
                'html': 'User already exists'}
            return render(request, 'registration/register.html', context=context)
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
            print(user, password)
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
        name = request.POST.get("name")
        steps = request.POST.getlist("steps")
        servings = request.POST.get("servings")
        image = request.FILES['image']
        prep_hour = int(request.POST.get("prep-time-hour"))
        prep_min = int(request.POST.get("prep-time-min"))
        cook_hour = int(request.POST.get("cook-time-hour"))
        cook_min = int(request.POST.get("cook-time-min"))
        ingredients = list(request.POST.getlist("ingredients"))
        image = request.FILES["image"]
        user = request.user
        prep_time = datetime.timedelta(hours=prep_hour, minutes=prep_min)
        cook_time = datetime.timedelta(hours=cook_hour, minutes=cook_min)
        recipe = Recipe(
            recipe_name=name,
            recipe_steps=steps,
            recipe_chef=user,
            recipe_servings=servings,
            recipe_prep_time=prep_time,
            recipe_cook_time=cook_time,
            recipe_image=image
        )
        r = recipe.save()
        for ingredient in ingredients:
            ing = Ingredient.objects.get(id = ingredient)
            recipe.recipe_ingredient.add(ing)

    elif request.method == "GET":
        pass
    Ingredients = Ingredient.objects.all()
    context = {
        'ingredients': Ingredients,
        'next' : next
    }
    return render(request,'recipe/add_recipe.html', context=context)


def view_recipes(request):
    recipes = Recipe.objects.all()
    context = { 'recipes' : recipes }
    return render(request, "recipe/view_recipes.html", context=context)


def recipe_details(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    steps=str(recipe.recipe_steps[2:-2]).split('\\r\\n')
    recipe.recipe_steps = steps
    ingredients = recipe.recipe_ingredient.all()
    context = { 'recipe' : recipe, 'ingredients' : ingredients }
    return render(request, "recipe/recipe_details.html", context=context)


@login_required
def add_ingredient(request):    
    if request.method == 'POST':
        name = request.POST.get("name")
        ing = Ingredient(ingredient_name=name)
        ing.save()
        return redirect('add-recipe')
    return render(request, 'recipe/add_ingredient.html')
