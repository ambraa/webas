from itertools import product
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .models import User
from .models import MenuListings
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm


class formCreateListing(ModelForm):
    class Meta:
        model = MenuListings
        fields = ["pavadinimas", "kaina", "nuotrauka"]
        widgets={
            'pavadinimas' :forms.TextInput(attrs={'class':'form-control'}),
            'kaina' :forms.NumberInput(attrs={'class':'form-control'}),  
        }

class formWatchlist(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["user", "product_id"]

def index(request):
    return render(request, "auctions/index.html",{
        "products": MenuListings.objects.all()
    })

def menu2(request):
    return render(request, "auctions/menu2.html",{
        "products": MenuListings.objects.all()
    })


def addwatchlist(request, product_id):
    if request.method == "POST":
        item = Watchlist()
        item.user = request.user.username
        item.product_id = product_id
        item.save()
        product = MenuListings.objects.get(id=product_id)
        watchlist = Watchlist.objects.filter(product_id=product_id, user = request.user.username)
        
        return render(request, "auctions/index.html",{
        "product": product,
        "watchlist": watchlist
        })
        
    else: 
        return render(request, "auctions/listing.html", {
            "form": formWatchlist()
        })
   


@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user = request.user.username)
    products = []
    for item in items:
        products.append(MenuListings.objects.get(id=item.product_id))
    empty = False
    if len(products) == 0:
        empty = True
    
    return render(request, "auctions/watchlist.html", {
        "empty": empty,
        "products": products
    }) 

def watchlist_remove(request, product_id):
    if request.method == "POST":
        item = Watchlist()
        item.user = request.user.username
        item.product_id = product_id
        product = MenuListings.objects.get(id=product_id)
        watchlist = Watchlist.objects.filter(product_id=product_id, user = request.user.username).delete()
        return render(request, "auctions/watchlist.html",{
        "product": product,
        "watchlist": watchlist
        })
        
    else: 
        return render(request, "auctions/listing.html", {
            "form": formWatchlist()
        })


def create_listing(request, ):
    if request.method == "POST":
        form = formCreateListing(request.POST, request.FILES)
        if form.is_valid():
            pavadinimas = form.cleaned_data["pavadinimas"]
            kaina = form.cleaned_data["kaina"]
            nuotrauka = form.cleaned_data["nuotrauka"]
            product = MenuListings(pavadinimas=pavadinimas, kaina=kaina, nuotrauka=nuotrauka)
            product.save()
             
    else: 
        return render(request, "auctions/create_listing.html", {
            "form": formCreateListing()
            
        }) 
           
    return render(request, "auctions/create_listing.html", {
            "form": formCreateListing()
        })  


def listing(request, product_id):
    product = MenuListings.objects.get(pk=product_id)
    return render(request, "auctions/listing.html", {
        "product": product
    })

def remove_listing(request, product_id):
    if request.method == 'POST':
        product=MenuListings()
        product.user = request.user.username
        product.product_id = product_id
        product = MenuListings.objects.get(pk=product_id).delete()
        product = MenuListings.objects.filter(product_id=product_id, user = request.user.username).delete()
        return render(request, "auctions/menu2.html",{
            "product": product
        })
    else: 
        return render(request, "auctions/menu2.html")


# def watchlist_remove(request, product_id):
#     if request.method == "POST":
#         item = Watchlist()
#         item.user = request.user.username
#         item.product_id = product_id
#         product = MenuListings.objects.get(id=product_id)
#         watchlist = Watchlist.objects.filter(product_id=product_id, user = request.user.username).delete()
#         return render(request, "auctions/watchlist.html",{
#         "product": product,
#         "watchlist": watchlist
#         })
        
#     else: 
#         return render(request, "auctions/listing.html", {
#             "form": formWatchlist()
#         })





# def uzsakymai(request):
#     # items = Watchlist.objects.all().order_by('user')
#     items = Watchlist.objects.all()
#     products = []
#     user=request.user.username
#     for item in items:
#         # print(item)
#         products.append(Watchlist.objects.get(id=item.product_id))
#     empty = False
#     if len(products) == 0:
#         empty = True
    
#     return render(request, "auctions/uzsakymai.html", {
#         "empty": empty,
#         "products": products,
#         "user": user
#     }) 

def uzsakymai(request):
    # items = Watchlist.objects.filter(user = request.user.username)
    items = Watchlist.objects.all().order_by('user')
    products = []
    users =[]
    for item in items:
        
        # products.append(item.user)
        products.append(MenuListings.objects.get(id=item.product_id))
        
        product_user = item.user
        if product_user not in users:
            users.append(product_user)
    empty = False
    if len(products) == 0:
        empty = True
    
    return render(request, "auctions/uzsakymai.html", {
        "empty": empty,
        "products": products,
        "users": users
    }) 









   



    






   




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")




# def categories(request):
#     return render(request, "auctions/categories.html",{
#         "categories": CATEGORY_CHOICES
#     })


# def category(request, category):
#     products = MenuListings.objects.all()

#     sameProducts = []

#     for product in products:
#         if product.category == category:
#             sameProducts.append(product)
#             empty = False
#             if len(products) == 0:
#                 empty = True

    

#     return render(request, "auctions/category.html", {
#         "products": sameProducts,
#         "category": category,
#         "empty":empty
#     })
