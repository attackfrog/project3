from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Pizza, PizzaTopping, Sub, SubTopping, OneSize, Platter, Order

# Create your views here.
def index(request):
    context = {
        "logged_in": request.user.is_authenticated
    }
    return render(request, "orders/index.html", context)

def login_view(request):
    context = {
        "logged_in": request.user.is_authenticated
    }
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"warning": "Invalid credentials."}, context)
    else:
        return render(request, "orders/login.html", context)

def logout_view(request):
    logout(request)
    context = {
        "logged_in": request.user.is_authenticated
    }
    return render(request, "orders/login.html", {"success": "Logged out."}, context)

def register_view(request):
    logout(request)
    if request.method == "POST":
        if not request.POST["password"] == request.POST["passconfirm"]:
            return render(request, "orders/register.html", {"warning": "Your passwords didn't match."})
        else:
            user = User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
            user.first_name = request.POST["firstname"]
            user.last_name = request.POST["lastname"]
            user.save()
            return render(request, "orders/login.html", {"success": "Account created! Please log in."})
    else:
        return render(request, "orders/register.html")

def menu_view(request):
    context = {
        "pizzas": Pizza.objects.all(),
        "subs": Sub.objects.all(),
        "oneSizes": OneSize.objects.all(),
        "platters": Platter.objects.all()
    }
    return render(request, "orders/menu.html", context)

def order_view(request):
    context = {
        "name": request.POST["item"],
        "type": request.POST["type"]
    }
    if context["type"] == "pizza":
        dbInfo = Pizza.objects.get(name=context["name"])
        context["numToppings"] = dbInfo.numToppings
        context["priceSmall"] = dbInfo.priceSmall
        context["priceLarge"] = dbInfo.priceLarge
        context["toppings"] = PizzaTopping.objects.all()
    elif context["type"] == "sub":
        dbInfo = Sub.objects.get(name=context["name"])
        context["priceSmall"] = dbInfo.priceSmall
        context["priceLarge"] = dbInfo.priceLarge
        if dbInfo.specialToppings:
            context["toppings"] = SubTopping.objects.all()
        else:
            context["toppings"] = [SubTopping.objects.get(name="Extra Cheese")]
    elif context["type"] == "oneSize":
        dbInfo = OneSize.objects.get(name=context["name"])
        context["price"] = dbInfo.price
    elif context["type"] == "platter":
        dbInfo = Platter.objects.get(name=context["name"])
        context["priceSmall"] = dbInfo.priceSmall
        context["priceLarge"] = dbInfo.priceLarge
        

    return render(request, "orders/order.html", context)
