from django.urls import path

from . import views

urlpatterns = [
    path("bid/", views.bid, name="bid"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<int:auction_id>/", views.listing, name="listing"),
    path("watchlist/<int:listing_id>/", views.watchlist, name="watchlist"),
    path("close/<int:listing_id>/", views.close, name="close"),
    path("user_won/<int:listing_id>/", views.user_won, name="user_won"),
    path("comment/<int:listing_id>/", views.comment, name="comment"),
    
    
]
