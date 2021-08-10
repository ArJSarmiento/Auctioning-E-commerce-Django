from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all, name="all"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("wishlist_add", views.wishlist_add, name="wishlist_add"),
    path("wishlist_remove", views.wishlist_remove, name="wishlist_remove"),
    path("wishlist_view", views.wishlist_view,name="wishlist_view"),
    path("close", views.close, name="close"),
    path("place_bid/<int:product_id>", views.place_bid, name="place_bid"),
    path("place_comment/<int:product_id>", views.place_comment, name="place_comment"),    
    path("<int:product_id>", views.listing_profile, name="listing_profile")
]
