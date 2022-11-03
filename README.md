# Project 2, Commerce

CS50W, Web Programming with Python and JavaScript

This project was prepared to satisfy Project 2, Commerce, in the online version of this class.

## Commerce - an eBay-like auction site

Implements and eBay-like commerce auction site that allows users to post auction listing, place bids on listings, comment on listings, and add listings to a watchlist. The basic functions of the app are:

- *Default page* Displays a list of all active (not closed) auctions.

- *Categories* Displays a list of available categories for auctions in the system. From that list, the user can click on the category names to be given a list of auctions in those categories.

- *Create Listing* Allows a logged-in user to create a new auction listing. [only for logged-in users]

- *My Watchlist* Displays a list of auction items on the user's watchlist  [only for logged-in users]

- *My Listings* Displays a list of all listings authored by the logged-in user [only for logged-in users]

- *Log Out* [only for logged-in users]

- *Log In*

- *Register*

- *Administrative functions* The built-in Django administrative app may be used to add, change, or delete data in the system.

## Technologies

The app is principally implemented with Python, Javascript, and the Django framework.

## Data Structure

The app uses the Django ORM framework for accessing a sqlite database using the following models:

```python
class User # built-in abstract user class
class Category # pre-defined permissible categories for auctions
class Bid
class Comment
class AuctionItem
```

## Usage

Run the app with the built-in Django server and the command `python3 manage.py runserver`



