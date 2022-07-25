from curses.ascii import HT
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from .forms import ContactForm, NewUserForm

# Create your views here.


def say_hello(request):
    return HttpResponse("Main view")


def homepage(request):
    return render(request, "main/home.html")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'niteshd@me.com',
                          ['niteshd@me.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("main:homepage")
    form = ContactForm()
    return render(request, "main/contact.html", {'form': form})

# User Registration Request


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})
