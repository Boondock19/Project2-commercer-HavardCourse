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
    Url_img=models.URLField(blank=True)
    Active=models.BooleanField(default=True)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="Categories")
    
    def __str__(self):
        return f"This is the listing title : {self.Title} created by {self.User}"

class Comment(models.Model):
    Listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="Listing_Comments")
    User=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_Comments")
    Contend=models.CharField(max_length=200)
    
    def __str__(self):
        return f"This is the comments of the user {self.User} in the Listing {self.Listing}"

class WathList(models.Model):
    pass

