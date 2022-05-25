

#pip install geopy
from geopy.geocoders import Nominatim
from geopy import distance
loc = Nominatim(user_agent="GetLoc")

def location(loc_1,loc_2,price):
    getLoc_1 = loc.geocode(f'{loc_1} Bangalore')
    getLoc_2 = loc.geocode(f'{loc_2} Bangalore')
    loc_1 = (getLoc_1.latitude,getLoc_1.longitude)
    loc_2 = (getLoc_2.latitude,getLoc_2.longitude)
    total_price = (distance.distance(loc_1, loc_2).km)*price
    return(total_price)

