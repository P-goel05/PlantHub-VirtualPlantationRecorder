"""
URL configuration for treeTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from treeApp import views

urlpatterns = [
    path('', views.home, name='home'), # default route
    path('admin/', admin.site.urls),
    # custom urls for treeApp
    path('home/', views.home, name='home'),
    path('forest_facts/', views.forest_facts, name='forest_facts'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),

    path('plant_tree/', views.plant_tree, name='plant_tree'),
    path('viewtree/', views.viewtree, name='viewtree'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('weather/', views.weather_view, name='weather'),
    path('predict_growth/', views.predict_growth, name='predict_growth'),
    path('nurseries/', views.nurseries, name='nurseries'),
]
