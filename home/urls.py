from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.index, name='landing'),
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('contact/',views.HomePage,name='contact'),
    path('logout/',views.LogoutPage,name='logout'),
] 