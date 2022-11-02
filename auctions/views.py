from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import  User, Category, Bid, AuctionItem, Comment


# default route
def index(request):
    allItems = AuctionItem.objects.filter(completed=False)
    context = {"itemList": allItems,
               "listName": "All Active Auctions"}
    return render(request, "auctions/index.html", context)

# route displayitem/
def displayitem(request):
    if request.method == "POST":
        itemid = request.POST["select"]
        myItem = AuctionItem.objects.get(itemId=itemid)
        mylisting = True if request.user == myItem.listedBy else False
        mywatched = True if request.user in myItem.watching.all() else False
        context = {
            "item": myItem,
            "mylisting": mylisting,
            "mywatched": mywatched
        }
        return render(request, "auctions/displayitem.html", context)

# route buttonprocess
def buttonprocess(request):
    if request.method == "POST":
        action = request.POST["process"]
        item = request.POST["itemid"]
        ai = AuctionItem.objects.get(itemId=item)
        if action == "close":
            ai.completed = True
        elif action == "remwatch":
            ai.watching.remove(request.user)
        else:
            # action == "addwatc":
            ai.watching.add(request.user)
        ai.save()
        return HttpResponseRedirect(reverse("index"))
        
    else:
        pass

# route categories/
def categories(request):
    if request.method == "POST":
        gcat = request.POST["mycat"]
        catList = AuctionItem.objects.filter(category=Category.objects.get(type=gcat))
        context = {"itemList": catList,
                   "listName": "Listings in " + gcat}
        return render(request, "auctions/index.html", context)
    else:
        cats = {"cats": Category.objects.all()}
        return render(request, "auctions/listcats.html", cats)

# route watchlist
def watchlist(request):
    if request.method == "POST":
        pass
    else:
        alls = list(AuctionItem.objects.all())
        mywatch = [anItem for anItem in alls if request.user in anItem.watching.all()]
        context = {"itemList": mywatch,
                   "listName": "My Watch List"}
        return render(request, "auctions/index.html", context)

def myitemlist(request):
    if request.method == "POST":
        pass
    else:
        alls = list(AuctionItem.objects.all())
        myitems = [anItem for anItem in alls if request.user == anItem.listedBy]
        context = {"itemList": myitems,
                   "listName": "My Auction Items"}
        return render(request, "auctions/index.html", context)

# route create/
def create(request):
    if request.method == "POST":
        name = request.POST["title"]
        description = request.POST["description"]
        starting = float(request.POST["starting"])
        category = Category.objects.get(type=request.POST["category"])
        listedBy = request.user
        pic = request.POST["image"]
        item = AuctionItem(name=name, description=description, starting=starting, category=category, 
                           listedBy = listedBy, pic=pic)
        item.save()
        return render(request, "auctions/index.html")
    else:
        return render(request, "auctions/create.html")

        

# route login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# route logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# route register 
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
