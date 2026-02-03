from urllib import request
from django.shortcuts import render , redirect
import requests 

from .models import PlantTree , Nursery , NurseryPlant , NurseryTool
from .forms import PlantTreeForm , TreeGrowthForm , TreeSelectForm

from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login , authenticate ,  logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import pickle
import os
# import django.conf import settings  

# Create your views here.
def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

@login_required
def plant_tree(request):
    if request.method == 'POST':
        form = PlantTreeForm(request.POST)
        if form.is_valid():
            tree=form.save(commit=False)
            tree.user= request.user
            tree.save()
            return redirect('plant_tree')
    else:
        form = PlantTreeForm()
    return render(request, 'plant_tree.html', {'form': form})

@login_required
def viewtree(request):
    trees = PlantTree.objects.filter(user=request.user).order_by('-planted_date')

    total_trees = trees.count()
    total_co2 = total_trees * 21      # kg CO2 per tree
    total_water = total_trees * 100   # liters per tree
    growth_percentage = min(total_trees * 10, 100)

    context = {
        'trees': trees,
        'total_trees': total_trees,
        'total_co2': total_co2,
        'total_water': total_water,
        'growth_percentage': growth_percentage,
    }

    return render(request, 'viewtree.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) #session created
            return redirect('home')
        else:
            return render(request, 'login.html', {'form': AuthenticationForm() , 'msg': 'Invalid credentials'})
    return render(request, 'login.html' , {'form': AuthenticationForm()}) 

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

def forest_facts(request):
    return render(request, 'forest_facts.html')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR,"tree_growth_model.pkl")

@login_required
def predict_growth(request):
    trees = PlantTree.objects.all()
    prediction = None

    if request.method == "POST":
        form = TreeGrowthForm(request.POST)
        if form.is_valid():
            tree_type = form.cleaned_data["tree_type"]
            avg_temp = form.cleaned_data["avg_temp"]
            water_freq = form.cleaned_data["water_freq"]

        # Load model
            with open(MODEL_PATH, "rb") as f:
                model, encoder = pickle.load(f)

            tree_type_encoded = encoder.transform([tree_type])[0]

            predicted_height = model.predict([[tree_type_encoded, avg_temp, water_freq]])
            prediction = round(predicted_height[0], 2)
    else:
        form=TreeGrowthForm()
        
    return render(request, "predict_growth.html", {
        'trees': trees,
        "form": form,
        "prediction": prediction
    })

@login_required
def nurseries(request):
    nurseries = Nursery.objects.filter(is_partnered=True)

    selected_nursery = None
    plants = None
    tools = None

    nursery_id = request.GET.get("nursery_id")

    if nursery_id:
        selected_nursery = Nursery.objects.get(id=nursery_id)
        plants = NurseryPlant.objects.filter(nursery=selected_nursery)
        tools = NurseryTool.objects.filter(nursery=selected_nursery)

    return render(request, "nurseries.html", {
        "nurseries": nurseries,
        "selected_nursery": selected_nursery,
        "plants": plants,
        "tools": tools
    })

@login_required
def weather_view(request):
    weather_data = None
    city = None
    selected_tree = None

    if request.method == "POST":
        form = TreeSelectForm(request.POST)
        if form.is_valid():
            selected_tree = form.cleaned_data["tree"]
            city = selected_tree.location
    else:
        form = TreeSelectForm()

    if city:
        API_KEY = "fdce9cc941cf47db632ce426354bc588"

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url)
        weather_data = response.json()

    context = {
        "form": form,
        "weather": weather_data,
        "city": city,
        "tree": selected_tree,
    }

    return render(request, "weather.html", context)