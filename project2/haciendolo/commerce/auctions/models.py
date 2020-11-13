from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    Category=models.CharField(max_length=20)

    def __str__(self):
        return self.Category

class Listing(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_Listing",default=None)
    Title=models.CharField(max_length=35)
    Description=models.CharField(max_length=200)
    Starting_Bid=models.FloatField()
    Price=models.FloatField(blank=True,null=True,default=None)
    Url_img=models.URLField(blank=True,default="https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png")
    Active=models.BooleanField(default=True)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="Categories")
    
    def __str__(self):
        return f"This is the listing title : {self.Title} created by {self.User}"

class Bid(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    Listing=models.ForeignKey(Listing,on_delete=models.CASCADE)
    bid_amount=models.FloatField()

    def __str__(self):
        return f"This is the bid of the user {self.User} and the bid is {self.bid_amount}"


class Comment(models.Model):
    Listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="Listing_Comments")
    User=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_Comments")
    Contend=models.CharField(max_length=200)
    
    def __str__(self):
        return f"This is the comments of the user {self.User} in the Listing {self.Listing}"

class WatchList(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_WatchList",blank=True,default=None)
    Listing=models.ManyToManyField(Listing,related_name="Listing_WatchList",blank=True)
    

    def __str__(self):
        return f"This is the watchlist of the user {self.User}"