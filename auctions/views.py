from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category, ClosedListing
from .utils.utils import get_active_listings, make_listing


def index(request):
    """
    Display the homepage with all active listings.
    
    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the index page with a list of active listings.
    """
    active_listings = get_active_listings()
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
    })


def login_view(request):
    """
    Handle user login functionality.
    
    Args:
        request: The HTTP request object, expecting POST data with 'username' and 'password'.

    Returns:
        HttpResponse: 
            - Renders the index page on successful login.
            - Renders the login page with an error message on failure.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    
    return render(request, "auctions/login.html")


def logout_view(request):
    """
    Log out the current user.
    
    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the index page after logout.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Handle user registration.
    
    Args:
        request: The HTTP request object, expecting POST data with 'username', 'email', 'password', and 'confirmation'.

    Returns:
        HttpResponse: 
            - Renders the index page on successful registration.
            - Renders the registration page with an error message if registration fails.
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            error_message = "Username or email already in use."
            if "username" in e.args[0]:
                error_message = "Username already taken"
            elif "email" in e.args[0]:
                error_message = "Email is already in use"

            return render(request, "auctions/register.html", {
                "message": error_message
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/register.html")


def create_listing(request):
    """
    Handle listing creation for authenticated users.
    
    Args:
        request: The HTTP request object, expecting POST data with listing details.

    Returns:
        HttpResponse: 
            - Renders the creation page for GET requests.
            - Renders the index page with a success message after successful listing creation.
            - Redirects to the index page if the user is not authenticated.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        make_listing(request)
        return render(request, "auctions/index.html", {
            "creation_msg": "Your listing has been created!"
        })
    
    return render(request, "auctions/create.html")


def check_listing(request, item_id):
    """
    Display details of a specific listing.
    
    Args:
        request: The HTTP request object.
        item_id (int): The ID of the listing to display.

    Returns:
        HttpResponse: Renders the listing page with details and comments.
    """
    listing = Listing.objects.get(pk=item_id)
    comments = Comment.objects.filter(listing=item_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })


def add_watchlist_item(request, item_id):
    """
    Add or remove a listing from the user's watchlist.
    
    Args:
        request: The HTTP request object.
        item_id (int): The ID of the listing to add or remove from the watchlist.

    Returns:
        HttpResponse: Redirects to the listing page after adding or removing the item.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        listing = Listing.objects.get(id=item_id)
        if request.user.watchlist.filter(id=item_id).exists():
            request.user.watchlist.remove(listing)
        else:
            request.user.watchlist.add(listing)

        return HttpResponseRedirect(reverse("listing", kwargs={"item_id": item_id}))


def watchlist(request):
    """
    Display the user's watchlist.
    
    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the watchlist page with the user's watchlist items.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    watchlist_items = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })


def bid(request, item_id):
    """
    Handle bidding on a listing.
    
    Args:
        request: The HTTP request object, expecting POST data with the bid amount.
        item_id (int): The ID of the listing to bid on.

    Returns:
        HttpResponse: 
            - Renders the listing page with a success message if the bid is successful.
            - Renders the listing page with an error message if the bid fails.
            - Redirects to the index page if the user is not authenticated.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    listing = Listing.objects.get(pk=item_id)

    if request.user == listing.owner:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "owner_error": "You cannot bid on your own listing!"
        })

    try:
        bid_amount = float(request.POST.get("bid_amount"))
    except ValueError:
        bid_amount = 0

    if bid_amount <= listing.highest_bid:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": bid_amount,
            "biding_error": "Your bid must be higher than the current price!"
        })

    listing.highest_bid = bid_amount
    listing.save()
    Bid.objects.create(amount=bid_amount, bider=request.user, item=listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "successfull_biding": "Your bid was successfully entered!",
    })


def close_listing(request, item_id):
    """
    Close a listing and declare a winner.
    
    Args:
        request: The HTTP request object.
        item_id (int): The ID of the listing to close.

    Returns:
        HttpResponse: Redirects to the listing page after closing it.
    """
    listing = Listing.objects.get(pk=item_id)

    if request.user != listing.owner:
        return HttpResponseRedirect(reverse("listing", kwargs={"item_id": item_id}))

    if Bid.objects.filter(item=item_id).exists():
        winner = Bid.objects.filter(amount=listing.highest_bid, item=listing.id).first().bider
    else:
        winner = request.user

    ClosedListing.objects.create(listing=listing, winner=winner)
    return HttpResponseRedirect(reverse("listing", kwargs={"item_id": item_id}))


def closed(request):
    """
    Display all closed listings.
    
    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the closed listings page with all closed listings.
    """
    closed_listings_ids = ClosedListing.objects.values_list("listing_id", flat=True)
    closed_listings = Listing.objects.filter(id__in=closed_listings_ids)
    return render(request, "auctions/closed.html", {
        "closed_listings": closed_listings
    })


def comment(request, item_id):
    """
    Add a comment to a listing.
    
    Args:
        request: The HTTP request object, expecting POST data with the comment content.
        item_id (int): The ID of the listing to comment on.

    Returns:
        HttpResponse: Redirects to the listing page after adding the comment.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("listing", kwargs={"item_id": item_id}))

    listing = Listing.objects.get(pk=item_id)
    content = request.POST.get("comment_content", "").strip()
    
    if content:
        Comment.objects.create(content=content, owner=request.user, listing=listing)

    return HttpResponseRedirect(reverse("listing", kwargs={"item_id": item_id}))


def categories(request):
    """
    Display all available categories.
    
    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the categories page with all categories.
    """
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):
    """
    Display all active listings in a specific category.
    
    Args:
        request: The HTTP request object.
        category (str): The name of the category to filter listings by.

    Returns:
        HttpResponse: Renders the category page with listings in the selected category.
    """
    category_obj = Category.objects.filter(category=category).first()
    if category_obj:
        category_listings = get_active_listings().filter(categories=category_obj)
    else:
        category_listings = Listing.objects.none()  # No listings if category not found

    return render(request, "auctions/category.html", {
        "category_listings": category_listings,
        "category": category
    })
