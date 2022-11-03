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
    #   Other
    categoryId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    
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
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mylistings")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, blank=True)
    starting = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    pic = models.URLField(max_length = 200, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    watching = models.ManyToManyField(User, blank=True, related_name="mywatching")
    
    def __str__(self):
        s = str(self.itemId) + " " + str(self.category) + " " + self.name
        if self.completed:
            s += " (completed)"
        else:
            s += " (active)"
        return s
