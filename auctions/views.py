from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction, Bid


def index(request):
    listings = Auction.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user) #creates session
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

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["starting_bid"]
        image = request.POST["image_url"]
        category = request.POST["category"]
        date = request.POST["created_date"]
        
        #create an object
        listing = Auction(
            title = title,
            description = description,
            starting_bid = bid,
            image_url = image,
            category = category,
            created_at = date,
            owner = request.user
        )
        listing.save() #save
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request, "auctions/create.html")    
 
 #get the details from the database in id format    
def listing(request, auction_id):
    listing = get_object_or_404(Auction, id=auction_id)
    highest_bid = listing.bids.order_by("-amount").first()
    if highest_bid:
        current_bid = highest_bid.amount
    else:
        current_bid = listing.starting_bid
    return render(request, "auctions/listing.html", {"listing": listing, "current_bid": current_bid})

@login_required
def watchlist (request, listing_id): 
    listing = Auction.objects.get(id=listing_id)
    
    if request.user in listing.watchlist.all(): #checks if user is in the watchlist
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)
        
    return redirect("listing", listing_id=listing_id) 

@login_required
def bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        bid_amount = float(request.POST["bid_amount"])
        listing = Auction.objects.get(id=listing_id)
        highest_bid = listing.bids.order_by("-amount").first() #gets the highestbid in the database but first it sorts
        
        if highest_bid:
            highest_amount = float(highest_bid.amount)
        else:
            highest_amount = float(listing.starting_bid)

        if bid_amount > highest_amount:

            Bid.objects.create(
                auction=listing,
                bidder=request.user,
                amount=bid_amount
            )

            message = "Yaaay, your bid has been placed successfully"

        else:
            message = "Oops! Your bid must be higher than the current bid"

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": message
        })

    return render(request, "auctions/listing.html")
       