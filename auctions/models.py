from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

CATEGORY_CHOICES = (
        ("fashion", "Fashion"),
        ("toys", "Toys"),
        ("electronics", "Electronics"),
        ("home", "home"),
    )

class MenuListings(models.Model):
    pavadinimas = models.CharField(max_length=64,)
    kaina = models.IntegerField()
    nuotrauka = models.ImageField(upload_to='images')  

    def __str__(self):
        return f"{self.id}, {self.pavadinimas}, {self.kaina}, {self.nuotrauka} "

class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid = models.IntegerField(max_length=64, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    # id = models.ManyToManyField(AuctionListings, blank=True)

    def __str__(self):
        return f"{self.id}:{self.user}, {self.comment}, {self.date}"
    

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    product_id = models.IntegerField()


    