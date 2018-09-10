from django.urls import path
from .import views

urlpatterns= [
    path('load_data/', views.load_data, name='load_data'),
]