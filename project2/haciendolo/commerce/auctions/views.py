from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

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
        ListingCreated.Price=ListingCreated.Starting_Bid
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
    user=request.user
    Listings=Listing.objects.all()
    ListingTarget=Listings.filter(id=pk)
    ListingWanted=ListingTarget[0]
    owned=Owner(user,ListingWanted)
    Bid_saved=41
    
    if request.method == "POST" :
        if "Close" in request.POST:
            CloseListing(ListingWanted)
            return HttpResponseRedirect(reverse("ListingPage",kwargs={'pk': ListingWanted.id }))

        if "New_Bid" in request.POST:
            if request.POST["New_Bid"]=="":
                messages.add_message(request, messages.ERROR, "Please enter a bid", extra_tags="bid_error")
                
                return HttpResponseRedirect(reverse("ListingPage",kwargs={'pk': ListingWanted.id }))
            else:
                New_Bid=int(request.POST["New_Bid"])
                
                
                if NewBid(New_Bid,user,ListingWanted) == True:
                    messages.add_message(request, messages.SUCCESS , "Your bid was save succesfully" , extra_tags="bid_message")
                    return HttpResponseRedirect(reverse("ListingPage",kwargs={'pk': ListingWanted.id }))
                    
                else:
                    messages.add_message(request, messages.ERROR, "Your bid should be higher than the actual price" , extra_tags="bid_message")
                    return HttpResponseRedirect(reverse("ListingPage",kwargs={'pk': ListingWanted.id }))
    else:
        context=({"Listing":ListingWanted,"owned":owned })
        return render(request,"auctions/ListingPage.html",context)


def Owner(user,Listing_obj):
    ListingTarget=Listing.objects.get(pk=Listing_obj.id)
    if user==ListingTarget.User:
        return True
    else:
        return False

def CloseListing(Listing_obj):
    ListingTarget=Listing.objects.get(pk=Listing_obj.id)
    ListingTarget.Active=False
    ListingTarget.save()

def NewBid(bid,user,Listing_obj):
    ListingTarget=Listing.objects.get(pk=Listing_obj.id)
    if bid > ListingTarget.Price:
        NewestBid=Bid()
        NewestBid.User=user
        NewestBid.bid_amount=bid
        NewestBid.Listing=ListingTarget
        NewestBid.save()
        Listing_obj.Price=NewestBid.bid_amount
        Listing_obj.save()
        return True
    else:
        return False
