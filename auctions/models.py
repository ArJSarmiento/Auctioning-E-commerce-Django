from django.contrib.auth.models import AbstractUser
from django.db import models

class Listing(models.Model):
    NOCATEGORY = 'NG'
    MENSAPPAREL = 'MA'
    WOMENSAPPAREL = 'WA'
    MOBILES = 'MB'
    SPORTS = 'SP'
    HOME = 'HM'
    TOYS = 'TY'
    
    CATEGORIES = [
        (NOCATEGORY, 'No Category'),
        (MENSAPPAREL, 'Mens Apparel'),
        (WOMENSAPPAREL, 'Womens Apparel'),
        (SPORTS, 'Sports'),
        (HOME, 'Home'),
        (TOYS, 'Toys')
    ]
    category =  models.CharField(
        max_length=2,
        choices  =CATEGORIES,
        default= NOCATEGORY,
    )

    isActive = models.BooleanField(default=True)
    name = models.CharField(max_length=255)    
    description = models.CharField(max_length=255)
    image = models.URLField(blank=True)
    starting_price = models.IntegerField(default = 0)
    current_price = models.IntegerField(default = 0)
    def __str__(self):
        return f"{self.name}"

    def get_label(CATEGORIES):
        return [c for c in CATEGORIES]


# DEFAULT_COMMENT_ID = 1
# class Comment(models.Model):
#     comment_listing =  models.ForeignKey(Listing,default=DEFAULT_COMMENT_ID, on_delete=models.CASCADE, related_name="comment_listing")
#     comment = models.CharField(max_length=255)
#     def __str__(self):

#         return f"{self.comment}"
    
class User(AbstractUser):
    my_watchlist =   models.ManyToManyField(Listing, blank=True, related_name="my_watchlist")
    my_listings = models.ManyToManyField(Listing, blank=True, related_name="my_listings")

DEFAULT_BID_ID = 1
class Bid(models.Model):
    bid = models.IntegerField(default = 0)
    bid_listing =  models.ForeignKey(Listing,default = DEFAULT_BID_ID, on_delete=models.CASCADE, related_name="bid_listing")
    bidder =  models.ForeignKey(User,default=DEFAULT_BID_ID, on_delete=models.CASCADE, related_name="bidder")
    def __str__(self):
        return f"{self.bid}"

DEFAULT_COMMENT_ID = 1
class Comment(models.Model):
    comment_listing =  models.ForeignKey(Listing,default=DEFAULT_COMMENT_ID, on_delete=models.CASCADE, related_name="comment_listing")
    commentor =  models.ForeignKey(User,default=DEFAULT_COMMENT_ID, on_delete=models.CASCADE, related_name="commentor")
    comment = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.comment}"