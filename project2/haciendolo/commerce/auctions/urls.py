from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CategoryList",views.Categories,name="Categories"),
    path("Category/<str:category>",views.CategoriesListing,name="CategoriesListing"),
    path("ListingPage/<int:pk>",views.ListingPage,name="ListingPage"),
    path("WatchList",views.WatchListPage,name="WatchList"),
    path("CreateListingPage",views.CreateListingPage,name="CreateListingPage")
]
