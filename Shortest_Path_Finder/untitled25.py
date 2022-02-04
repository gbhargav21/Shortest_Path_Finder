# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:28:45 2021

@author: BHARGAV
"""

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.reverse("16.498659370671454,80.65388506932013")

print(location)
