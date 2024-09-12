from django.urls import path
from .views import *

urlpatterns = [
    
    path('predicts/', predicts, name='predicts'),
    
]
