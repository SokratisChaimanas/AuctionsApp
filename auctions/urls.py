from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create"),
    path("listing/<int:item_id>", views.check_listing, name="listing"),
    path("watchlist/<int:item_id>", views.add_watchlist_item, name="add_watchlist_item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("close_listing/<int:item_id>", views.close_listing, name="close_listing"),
    path("closed", views.closed, name="closed"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category")
]
