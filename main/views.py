"""
This views.py is under main app 
 """
from curses.ascii import HT
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import ContactForm, NewUserForm

# Create your views here.

articles = {
    'sports': 'Sports Pages',
    'food': 'Food Pages',
    'politics': 'Politics Pages',
    'finance': 'Finance Pages',
}

"""
Generic view for any articles
"""


def news_view(request, topic):
    try:
        result = articles[topic]
        return HttpResponse(articles[topic])
    except:
        result = '<h1>No page found for that topic {}!</h1>'.format(topic)
        # return HttpResponseNotFound(result)
        raise Http404(result)


"""
Redirect users using numeric value to actual page
"""


def num_page_view(request, num_page):
    # try:
    #     topic_list = list(article.keys())  # ['sports', 'food', etc]
    #     topic = topic_list[num_page]
    #     return HttpResponseRedirect(topic)
    # except:
    #     result = '<h1>No page found for that topic {}!</h1>'.format(topic)
    #     return HttpResponseNotFound(result)
    topic_list = list(articles.keys())  # ['sports', 'food', etc]
    topic = topic_list[num_page]

    return HttpResponseRedirect(reverse('topic-page', args=[topic]))

# Testing title


def variable_view(request):
    return render(request, 'main/header.html', context={'title': 'Home'})


def say_hello(request):
    return HttpResponse("Main view")


def homepage(request):
    return render(request, "main/home.html", context={'title': 'Landing Page'})


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
            return redirect("main:login")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form, 'title': 'Register'})


# User Login Request Form
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form, "title": "User Login"})


# User Logout Request
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:home")
