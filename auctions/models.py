from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extends the default Django user model by adding an email field that must be unique 
    and a many-to-many relationship with Listing to represent the user's watchlist.
    """
    email = models.EmailField(unique=True)
    watchlist = models.ManyToManyField("Listing", related_name="watchers")


class Category(models.Model):
    """
    Represents a category for listings. Each category has a name.
    """
    category = models.CharField(max_length=254)

    def __str__(self) -> str:
        return self.category


class Listing(models.Model):
    """
    Represents an auction listing with various fields such as title, description, 
    starting bid, highest bid, image, categories, and creation timestamp.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=10000)
    starting_bid = models.FloatField()
    highest_bid = models.FloatField()
    image = models.URLField(max_length=1024, null=True)
    categories = models.ManyToManyField(Category, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    """
    Represents a bid on a listing, with a relationship to the user who placed the bid 
    and the item that was bid on.
    """
    amount = models.FloatField()
    bider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")


class Comment(models.Model):
    """
    Represents a comment on a listing, associated with a user and a specific listing. 
    Includes the comment content and a timestamp of when it was created.
    """
    content = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)


class ClosedListing(models.Model):
    """
    Represents a closed auction listing, linking the listing to the user who won it.
    """
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="closed_listing")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winned_listings", default=None)
