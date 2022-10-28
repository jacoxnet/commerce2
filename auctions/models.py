from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    # Categories of AuctionItems
    # Known categories now are 
    #   Household
    #   Electronics
    #   Computers
    #   Tools
    #   Autos
    categoryId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.type

class Bid(models.Model):
    bidId = models.AutoField(primary_key=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bidAmount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

class AuctionItem(models.Model):
    itemId = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    bids = models.ManyToManyField(Bid, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    starting = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    pic = models.URLField(max_length = 200, blank=True)
    
    def __str__(self):
        s = str(self.category) + " " + self.name
        if self.completed:
            s += " (completed)"
        else:
            s += " (active)"
        return s
