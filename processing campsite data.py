#this changes information by campsite into general campground info
import requests
import json
import pandas as pd

def getcampsitedata(campground_id):
  headers = {'Content-type': 'application/json', "apikey": "f5e1e19c-fb0f-4585-b080-09b688d535eb"} 
  r = requests.get(f'https://ridb.recreation.gov/api/v1/facilities/{campground_id}/campsites?limit=10&offset=0', headers = headers)
  data = r.json()
  
  for thing in data["RECDATA"]:
    site_types = set()
    amenity_list = set()
    additional_features = set()
    regulations = set()
    reservable = False
    pet_friendly = False
    ada_accessible = False
    for attribute in thing["ATTRIBUTES"]:
          site_types = set()
          if attribute == {'AttributeName': 'Picnic Table', 'AttributeValue': 'Y'}:
            amenity_list.add("picnic tables")
          if attribute == {'AttributeName': 'CAMPFIRE RINGS', 'AttributeValue': 'Campfire Rings'} or attribute == {'AttributeName': 'Fire Pit', 'AttributeValue': 'Y'}:
            amenity_list.add("fire rings")
          if attribute == {'AttributeName': 'FOOD STORAGE LOCKER', 'AttributeValue': 'Food Storage Locker'}:
            amenity_list.add("food storage lockers")
          if attribute == {'AttributeName': 'Pets Allowed', 'AttributeValue': 'Yes'}:
            pet_friendly = True

    if thing["CampsiteAccessible"] == "TRUE":
              ada_accessible = True
  
    if thing["CampsiteReservable"] == "TRUE":
              reservable = True
    site_types.add(thing["CampsiteType"])

    #print(f"Campground has following campisite types: {site_types}, amenities include {amenity_list} ENJOY YOUR STAY")

    return site_types, amenity_list, additional_features

def get_facilites_by_rec_area(area_id):
  headers = {'Content-type': 'application/json', "apikey": "f5e1e19c-fb0f-4585-b080-09b688d535eb"} 
  r = requests.get(f'https://ridb.recreation.gov/api/v1/recareas/{area_id}/facilities?limit=1000&offset=0', headers = headers)
  data = r.json()
  for thing in data["RECDATA"]:
    camp_name = str()
    reservable = False
    ada_accessible = False
    camp_name = thing["FacilityName"]
    if thing["Reservable"] == "True":
      reservable = True
    if thing["FacilityAdaAccess"] == "True":
      ada_accessible = True  
    campground_id = thing["FacilityID"]
    print(camp_name + " reservable = " + f'{reservable}')

    amenities = set()

    site_types, campsite_amenities, additional_features = getcampsitedata(campground_id)

    amenities.union(campsite_amenities)
    
#Request URLs
#Rec areas: https://ridb.recreation.gov/api/v1/recareas?limit=50&offset=0
#Facilities: https://ridb.recreation.gov/api/v1/facilities?limit=10&offset=0
#all facilities of a rec area https://ridb.recreation.gov/api/v1/recareas/2907/facilities?limit=1000&offset=0
#all campsites of a facility https://ridb.recreation.gov/api/v1/facilities/233742/campsites?limit=50&offset=0
#all addresses of a facility https://ridb.recreation.gov/api/v1/facilities/259196/facilityaddresses?limit=50&offset=0
#all activities for a facility https://ridb.recreation.gov/api/v1/facilities/233742/activities?limit=50&offset=0



area_id = 2907
get_facilites_by_rec_area(area_id)





#CAMPGROUND NAME is a BASIC/PRIM/DEVELOPED campground in AREA. 
#This campground in AREA has RESERVABLE Y/N CAMPSITE TYPE sites, some of which feature ATTRIBUTE (views)
# The facility offers RESERVABLE Y/N CAMPSITE TYPE sites 
# and offers a chance to enjoy ACTIVITY ACTIVITY ACTIVITY in the summer, as well as ACTIVITY ACTIVITY ACTIVITY in the winter.
#In summer, campers can enjoy ACTIVITY ACTIVITY ACTIVITY in the summer, while in winter, ACTIVITY ACTIVITY ACTIVITY are available."""