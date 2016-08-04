import requests, urllib

'''
TODO:
  * add all currencies supported by the Steam Marketplace to `curAbbrev`
  * create docstrings for all functions
  * listings parser; get total number of listings (`total_count` in JSON);
     will be different for keys and cases
  * get price overview via http://steamcommunity.com/market/priceoverview/
  * add alternative price grabbing function for keys and cases, as they are as
     not sold as individual listings and hence do not show more than one
     listing when `MarketItem.get_listing()` is called.
  * add function to check if Steam thinks you have made too many requests
'''

# Currency abbreviations
curAbbrev = {
    'USD' : 1,
    'GBP' : 2,
    'EUR' : 3,
    'CHF' : 4,
    'RUB' : 5,
    'KRW' : 16,
    'CAD' : 20,
}

class MarketListing:
    def __init__(self, listing_id, price):
        self._id = listing_id
        self.price = price

class MarketItem:
    """
    Initialize MarketItem

    @param game_id: Numeric ID of Steam game item is associated with.
    @param item_name: Name of item as per its listing on the Steam Market.
        This must include all spaces, special characters, and casing.
        Otherwise data pulled for item may be skewed or null.
    """
    def __init__(self, game_id, item_name):
        self.game_id = game_id
        self.item_name = item_name
        self.listings = []

    """
    Adds a market listing for item. Avoid using this, as it is only meant
    for internal use by `get_listings`.

    @param l_id: ID of listing on the Steam Market.
    @param price: Price of item on the Steam Market.
    """
    def add_listing(self, l_id, price):
        self.listings.append(MarketListing(l_id, price))

    """
    Clears all listings.
    """
    def clear_listings(self):
        self.listings = []

    """
    Gets item listings from the Steam Marketplace. Listings will be stored in
    `self.listings` Depending on your chosen currency, you may need to
    move the decimal place of listing prices. For instance, in USD, $25.98
    would be returned as 2598. Only one listing will show up for items like
    keys and cases. This is the 

    @param game_id: ID of game item belongs to.
    @param item: Name of item to lookup.
    @param start: Listing index to start from. 0 is the most recent listing.
    @param start: number >= 0
    @param count: Number of listings to grab, start and beyond.
    @param count: number >= 1
    @param currency: Abbreviation of currency to return listing prices in.
    @type currency:
        Accepted currencies:

          - USD
          - GBP
          - EUR
          - CHF
          - RUB
          - KRW
          - CAD

        Please lookup the proper abbreviation for your currency of choice.
    """
    def get_listings(self, start=0, count=10, currency='USD'):
        url = 'http://steamcommunity.com/market/listings/{}/{}/render'.format(
            self.game_id,
            urllib.parse.quote(self.item_name)
        )
        payload = {
            'start' : start,
            'count' : count,
            'currency' : curAbbrev[currency]
        }
        resp = requests.get(url, params=payload)
        new_listings = resp.json()['listinginfo']
        for l_id, v in new_listings.items():
            price = v['converted_price_per_unit'] + v['converted_fee_per_unit']
            self.add_listing(l_id, price)

"""
Create a MarketItem for TF2.

@param item_name: Name of item as per its listing on the TF2 Market.
"""
def get_tf2_item(item_name):
    return MarketItem(440, item_name)

"""
Create a MarketItem for CS:GO.

@param item_name: Name of item as per its listing on the CS:GO Market.
"""
def get_csgo_item(item_name):
    return MarketItem(730, item_name)
