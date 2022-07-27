"""
This urls.py is under main app 
 """

from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="home"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.say_hello, name='login'),
    path('register/', views.register_request, name="register"),
    path('title/', views.variable_view),
    path('<int:num_page>/', views.num_page_view),
    path('<str:topic>/', views.news_view, name='topic-page'),


]
