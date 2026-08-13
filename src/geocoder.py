"""
    Name: Graph Navigator
    Copyright: © Georgios Pegiazis 2026
    Author: Georgios Pegiazis (https://github.com/GeorgePeg)
    Date: 12/08/2026
    Version: 1.0.0
    License: GNU General Public License v3.0, 29 June 2007
    Description: Εδώ μετατρέπονται οι πραγματικές διευθύνσεις σε γεωγραφικές συντεταγμένες.
"""
from typing import Tuple, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Κλάση μετατροπής διευθύνσεων σε συντεταγμένες
class Geocoder:
    def __init__(self, user_agent: str = "graph_navigator_app"):
        self.geolocator = Nominatim(user_agent=user_agent)
    def geocode(self, address: str) -> Optional[Tuple[float, float]]:
        try:
            location = self.geolocator.geocode(address, timeout=10)
            if location:
                return location.latitude, location.longitude
            else:
                return None, f"Σφάλμα: Η διεύθυνση {address} δεν βρέθηκε!"
        except (GeocoderTimedOut,GeocoderServiceError) as e:
            return None, print(e)