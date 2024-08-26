from ..models import Listing, ClosedListing, Category
    

def get_active_listings():
    closed_listings = ClosedListing.objects.all()
    closed_listing_ids = list(closed_listings.values_list('listing_id', flat=True))
    active_listings = Listing.objects.all().exclude(id__in=closed_listing_ids)
    return active_listings


def make_listing(request):
    owner = request.user
    title = request.POST.get("title")
    description = request.POST.get("description")
    starting_bid = float(request.POST.get("starting_bid"))
    
    # Storing iformation to the listing.
    listing = Listing.objects.create(owner=owner, title= title, description= description, starting_bid=starting_bid, highest_bid=starting_bid)

    listing.title = request.POST.get("title")
    listing.description = request.POST.get("description")
    listing.starting_bid = int(request.POST.get("starting_bid"))

    if request.POST.get("image"):
        listing.image = request.POST.get("image")
    if request.POST.getlist("categories[]"):
        for category in request.POST.getlist("categories[]"):
                category, created = Category.objects.get_or_create(category=category)
                listing.categories.add(category)
                
    listing.save()
