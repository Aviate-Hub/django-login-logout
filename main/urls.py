"""
This urls.py is under main app 
 """

from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.say_hello),
    path('register/', views.register_request, name="register"),
    path('sports/', views.sports_view),
    path('finance/', views.finance_view)

]
