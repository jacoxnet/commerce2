from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import User, Category, Bid, AuctionItem, Comment


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
        action = request.POST["process"] if "process" in request.POST else "pass"
        print ('action is ', action)
        if action == "close":
            myItem.completed = True
            myItem.save()
        elif action == "remwatch":
            myItem.watching.remove(request.user)
            myItem.save()
        elif action == "addwatch":
            myItem.watching.add(request.user)
            myItem.save()
        elif action == "relist":
            myItem.completed = False
            myItem.save()
        else:
            # action must be pass
            pass
        itemstatus, userstatus, watchstatus, comments = getstatus(request, myItem)
        context = {
            "item": myItem,
            "itemstatus": itemstatus,
            "userstatus": userstatus,
            "watchstatus": watchstatus,
            "comments": comments
        }
        return render(request, "auctions/displayitem.html", context)

# helper function getstatus()
def getstatus(request, item):
    if not item.completed:
        itemstatus = "Active"
    else:
        itemstatus = "Sold" if item.bid else "Closed unsold"
    userstatus = None
    watchstatus = False
    if request.user.is_authenticated:
        if request.user == item.listedBy:
            userstatus = "seller" if item.completed else "lister"
        if item.bid and request.user == item.bid.bidder:
            userstatus = "buyer" if item.completed else "high bidder"
        if request.user in item.watching.all():
            watchstatus = True
    comments = item.comments.all()
    return itemstatus, userstatus, watchstatus, comments

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

# route enterbid/
def enterbid(request):
    if request.method == "POST":
        bidamt = float(request.POST["bidamt"])
        print('bid is ', bidamt)
        item = request.POST["myitem"]
        myItem = AuctionItem.objects.get(itemId=item)
        if (bidamt < myItem.starting) or (myItem.bid and bidamt <= myItem.bid.bidAmount):
            message = "Bid too low"
            print(message)
        else:
            b = Bid(bidder=request.user, bidAmount=bidamt)
            b.save()
            myItem.bid = b
            myItem.save()
            message = "Valid bid entered"
            print(message)
        itemstatus, userstatus, watchstatus, comments = getstatus(request, myItem)
        context = {
            "item": myItem,
            "itemstatus": itemstatus,
            "userstatus": userstatus,
            "watchstatus": watchstatus,
            "comments": comments,

            "messages": [message]
        }
        return render(request, "auctions/displayitem.html", context)
        
# route addcomment/
def addcomment(request):
    if request.method == "POST":
        comment = request.POST["newcomment"]
        print("new comment", comment)
        item = request.POST["myitem"]
        myItem = AuctionItem.objects.get(itemId=item)
        c = Comment(user=request.user, text=comment)
        c.save()
        myItem.comments.add(c)
        myItem.save()
        itemstatus, userstatus, watchstatus, comments = getstatus(request, myItem)
        context = {
            "item": myItem,
            "itemstatus": itemstatus,
            "userstatus": userstatus,
            "watchstatus": watchstatus,
            "comments": comments,
        }
        return render(request, "auctions/displayitem.html", context)

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
        starting = request.POST["starting"]
        if not name or not description or not starting:
            messages = ["Name, description, and minimum bid must be specified"]
            cats = Category.objects.all()
            return render(request, "auctions/create.html", {"messages": messages, "cats": cats})
        starting = float(starting)
        listedBy = request.user
        category = request.POST["category"]
        if category == "Select the category":
            category = "Other"
        category = Category.objects.get(type=category)
        pic = request.POST["image"]
        if not pic:
            # representation of no pic
            pic = "https://live.staticflickr.com/65535/52471214195_90f244ca67_o_d.png"
        item = AuctionItem(name=name, description=description, starting=starting, category=category, 
                           listedBy = listedBy, pic=pic)
        item.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        cats = {"cats": Category.objects.all()}
        return render(request, "auctions/create.html", cats)

        

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
                "messages": ["Invalid username and/or password."]
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
                "messages": ["Passwords must match."]
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "messages": ["Username already taken."]
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
