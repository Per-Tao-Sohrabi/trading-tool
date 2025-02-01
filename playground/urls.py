# This module maps urls to view functions. 
from django.urls import path
from . import views # So we can refernce our view funciton

# URLConf
urlpatterns = [
    path('hello/', views.hello)
]