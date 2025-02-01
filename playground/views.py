from django.shortcuts import render
from django.http import HttpResponse

# Request handler
# Reeqest -> response
# Note: A view funciton is a function that takes a request and returns a response.  
# Create your views here.
# Is not a template

def hello(request): # takes request and returns a response.
    # can pull data, can send email whatever.
    return HttpResponse("Hello World") # Now map this funciton to a url. When we get a request from a url, this function will be called. 

