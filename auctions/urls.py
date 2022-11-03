from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("displayitem", views.displayitem, name="displayitem"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("myitemlist", views.myitemlist, name="myitemlist"),
    path("enterbid", views.enterbid, name="enterbid"),
    path("addcomment", views.addcomment, name="addcomment")
]
