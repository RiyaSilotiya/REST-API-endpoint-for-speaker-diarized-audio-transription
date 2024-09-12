from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def Home(request):
    return HttpResponse("hiii world shitru beta KSNL NEWhvk.")

def page(request):
    return HttpResponse("<h1>hi shitru</h1>")