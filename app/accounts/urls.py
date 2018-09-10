from django.urls import path

from .import views

urlpatterns= [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('test_auth/', views.test_auth, name='test_auth'),
    path('logout/', views.logout, name='logout'),
]