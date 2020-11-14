from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    Active_Listing=Listing.objects.filter(Active=True)
    context=({
        "Listings":Active_Listing
    })
    return render(request, "auctions/index.html",context)


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

def Categories(request):
    Categories=Category.objects.all()
    return render(request,"auctions/category.html",({
        "categories":Categories
    }))

def CategoriesListing(request,category):
    Listings=Listing.objects.filter(Category__Category=category,Active=True)

    return render(request,"auctions/categoryListing.html",({
        "Listings":Listings
    }))

def WatchListPage(request):
    user_target=User.objects.get(username=request.user)
    try:
        watchlist_target=WatchList.objects.get(User=user_target)
    except (UnboundLocalError, WatchList.DoesNotExist):
        watchlist_target=WatchList()
        watchlist_target.User=user_target
        watchlist_target.save()
    
    context=({"Listings": watchlist_target.Listing.all()})
    return render(request,"auctions/WatchList.html",context)

def CreateListingPage(request):
    ListofListings=Listing.objects.all()
    Categories=Category.objects.all()
    message=""
    if request.method=="POST":
        ListingCreated=Listing()
        ListingCreated.User=request.user
        ListingCreated.Title=request.POST["title"]
        ListingCreated.Description=request.POST["description"]
        ListingCreated.Starting_Bid=request.POST["startingbid"]
        ListingCreated.Category=Category.objects.get(Category=request.POST["category"])
        if request.POST["imgurl"]=="":
            ListingCreated.Url_img="https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png"
        #if ListingCreated.Title in
        else: 
            ListingCreated.Url_img=request.POST["imgurl"] 
        
        for e in ListofListings:
            if ListingCreated.Title==e.Title:
                message="This Listing already exist"
                break
        if message != "":
            context=({"message":message,"Title":ListingCreated.Title,
            "Description":ListingCreated.Description,"StartingBid":ListingCreated.Starting_Bid,
            "Categories":Categories })
            
            return render(request,"auctions/CreateListingPage.html",context)
        
        ListingCreated.save()
        
        
        return HttpResponseRedirect(reverse("index"))
    
    else:
        
        context=({"Categories":Categories})
        return render(request,"auctions/CreateListingPage.html",context)

def ListingPage(request,pk):
    Listings=Listing.objects.all()
    ListingTarget=Listings.filter(id=pk)
    ListingWanted=ListingTarget[0]
    #return print(ListingTarget[0].Title)
    context=({"Listing":ListingWanted})
    return render(request,"auctions/ListingPage.html",context)


