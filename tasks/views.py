from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Hello, world.")
def contact(request):
    return HttpResponse("From contact.")
def show_task(request):
    return HttpResponse("From task.")