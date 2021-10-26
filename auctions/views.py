from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.fields import URLField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django import forms
from .models import User, Bid, Comment, Listing
from django.db.models import Max, aggregates, fields
from django.contrib.auth.decorators import login_required

class CommentForm(forms.ModelForm):
    comment = forms.CharField( label='')
    class Meta:
        model = Comment
        fields = ['comment']

class BidForm(forms.ModelForm):
    bid = forms.IntegerField(label='',
    required=False,
    widget=forms.TextInput(attrs={ 'required': 'false' }))
    class Meta:
        model = Bid
        fields = ['bid']

class ListingForm(forms.ModelForm):
    description = forms.CharField( label='')
    name = forms.CharField( label='')
    image= forms.URLField ( label='', required=False)
    starting_price = forms.IntegerField(label='')
    class Meta:
        model = Listing
        fields= ['description', 'name', 'image', 'starting_price', 'category']
        widgets = {
            'category': forms.Select(choices=Listing.CATEGORIES,attrs={'class': 'form-control'}),
            'description':forms.TextInput(attrs={'class': 'form-description'}),
            'name': forms.TextInput(attrs={'class': 'form-name'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-starting_price'})
        }

class DropdownForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category']
           
def isInWatchlist(current_user, product):
    return product in current_user.my_watchlist.all()

def index(request):
    listings = Listing.objects.filter(isActive = True)
    categories = Listing.get_label(Listing.CATEGORIES)
    current_user = request.user
    if request.method == "POST":
        c =  request.POST.get("categories")
        if c != "all":
            listings = Listing.objects.filter(category__icontains = c)
            data = {
                "current_category": c,
                "listings": listings,
                "categories": categories,
            }
            if current_user.is_authenticated:
                data["watchlist_items"] = current_user.my_watchlist.all()
            return render(request, "auctions/index.html", data)
    data = {
        "listings": listings,
        "categories": categories
        }
    if current_user.is_authenticated:
            data["watchlist_items"] = current_user.my_watchlist.all()
    return render(request, "auctions/index.html", data)

def all(request):
    listings = Listing.objects.all()
    categories = Listing.get_label(Listing.CATEGORIES)
    current_user = request.user
    if request.method == "POST":
        c =  request.POST.get("categories")
        if c != "all":
            listings = Listing.objects.filter(category__icontains = c)
            data = {
                "current_category": c,
                "listings": listings,
                "categories": categories
            }
            if current_user.is_authenticated:
                data["watchlist_items"] = current_user.my_watchlist.all()

            return render(request, "auctions/all.html", data)

    data = {
        "listings": listings,
        "categories": categories
    }
    if current_user.is_authenticated:
        data["watchlist_items"] = current_user.my_watchlist.all()
    return render(request, "auctions/all.html", data)

def get_all_inwatchlist(listings, c):
    return [product for product in listings 
        if (product in Listing.objects.filter(category__icontains = c))]

def listing_profile(request, product_id):
    product =  Listing.objects.get(id = product_id)
    current_user = request.user
    all_comments = Comment.objects.filter(comment_listing = product)
    _isActive = product.isActive
    data = {     
        "WinnerName": current_user,
        "isActive": _isActive,
        "bid_isvalid" : True,
        "comments": all_comments,
        "has_content": True,
        "product": product,
        "commentform": CommentForm(),
        "bidform": BidForm(initial={'bid': product.current_price}),
    }

    if current_user.is_authenticated:
        InWatchlist = isInWatchlist(current_user, product)
        isMine = product in current_user.my_listings.all()

        args = Bid.objects.filter(bid_listing=product)
        if args.count() >= 1:
            highest_bid =  args.order_by('-bid')[0]
            isWinner = highest_bid.bidder == current_user
            data["isWinner"] = isWinner


        data["in_watchlist"] = InWatchlist
        data["isMine"] = isMine

    return render(request, "auctions/profile.html", 
        data
    )

@login_required(login_url='login')
def close(request):
    if request.method == "POST":
        form = request.POST.get("product_id")
        product =  Listing.objects.get(id = form)
        product.isActive = False
        product.save()
        return redirect('/' + str(form))

@login_required(login_url='login')
def place_bid(request, product_id):
    product =  Listing.objects.get(id = product_id)
    all_comments = Comment.objects.filter(comment_listing = product)
    current_user = request.user
    InWatchlist = isInWatchlist(current_user, product)

    if request.method == "POST":
        bidform = BidForm(request.POST or None)
        if bidform.is_valid() and bidform != None:
            added_bid  = bidform.save(commit=False)
            if (
                added_bid.bid < product.starting_price
                or added_bid.bid <= product.current_price
            ):
                return render(request, "auctions/profile.html",{
                    "WinnerName": current_user,
                    "isActive": True,
                    "bid_isvalid" : False,
                    "comments": all_comments,
                    "has_content": True,
                    "product": product,
                    "bidform": BidForm(),
                    "commentform": CommentForm(),
                    "in_watchlist": InWatchlist
                }) 

            added_bid.bid_listing = product
            added_bid.bidder = current_user
            added_bid.save()
            product.current_price = added_bid.bid
            product.save()
    return redirect('/' + str(product_id))

@login_required(login_url='login')
def place_comment(request, product_id):
    product =  Listing.objects.get(id = product_id)
    current_user = request.user

    if request.method == "POST":
        commentform = CommentForm(request.POST or None)
        if commentform.is_valid() and commentform != None:
            added_comment  = commentform.save(commit=False)
            added_comment.comment_listing = product
            added_comment.commentor = current_user
            added_comment.save()

    return redirect('/' + str(product_id))

@login_required(login_url='login')
def create(request):
    current_user = request.user
    categories = Listing.get_label(Listing.CATEGORIES)

    if request.method == "POST":
        listingform =ListingForm(request.POST)
        if listingform.is_valid():
            added_listing = listingform.save(commit= False)
            added_listing.isActive = True
            added_listing.current_price =  added_listing.starting_price
            if added_listing.image == "" or added_listing.image is None:
                added_listing.image = "https://gailperrygroup.com/wp-content/uploads/2012/05/auction-gavel-1.jpg"
            added_listing.save()
            current_user.my_listings.add(added_listing)
            return redirect("/"+str(added_listing.id))
        else:
            data ={
                "listingform": listingform,
                "categories": categories
            }
            return render(request, "auctions/create.html", 
                data
            )
    else:
        data ={
            "listingform": ListingForm(),
            "categories": categories
        }
        return render(request, "auctions/create.html", 
            data
        )

@login_required(login_url='login')
def wishlist_add(request):
    if request.method == "POST":
        current_user = request.user
        form = request.POST.get("product_id")
        product =  Listing.objects.get(id = int(form))
        current_user.my_watchlist.add(product)
        return redirect("/"+form)

@login_required(login_url='login')
def wishlist_remove(request):
    if request.method == "POST":
        current_user = request.user
        form = request.POST.get("product_id")
        product =  Listing.objects.get(id = int(form))
        current_user.my_watchlist.remove(product)
        return redirect("/"+form)

@login_required(login_url='login')
def wishlist_view(request):
    categories = Listing.get_label(Listing.CATEGORIES)
    current_user = request.user
    listings = current_user.my_watchlist.all()
    if request.method == "POST":
        c =  request.POST.get("categories")
        if c != "all":
            listings = get_all_inwatchlist(listings, c)
        data = {
            "current_category": c,
            "listings": listings,
            "categories": categories
        }
    else:
        data ={
            "wishlist": current_user, 
            "listings": listings,
            "categories": categories
        }

    return render(request, "auctions/wishlist.html", data)
    
def login_view(request):
    if request.method != "POST":
        return render(request, "auctions/login.html")

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

        # Check if authentication successful
    if user is None:
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method != "POST":
        return render(request, "auctions/register.html")
        
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
