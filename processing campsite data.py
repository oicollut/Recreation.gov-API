import requests
import json
import pandas as pd
import random

def getcampactivities(campground_id):
  headers = {'Content-type': 'application/json', "apikey": "************************"} 
  r = requests.get(f'https://ridb.recreation.gov/api/v1/facilities/{campground_id}/activities?limit=10&offset=0', headers = headers)
  data = r.json()
  activities = set()
  for thing in data["RECDATA"]:
      activities.add(thing["FacilityActivityDescription"].lower())
  
  activity_type_dict = sorted_activities()
  winter_values = []
  summer_values = []
  water_values = []
  cultural_values = []
  newdict = {}
  for activity in activities:
    if activity in activity_type_dict["water activity"]:
      water_values.append(activity)
    if activity in activity_type_dict["winter activity"]:
      winter_values.append(activity)
    if activity in activity_type_dict["cultural activity"]:
      cultural_values.append(activity)
  newdict["water activities"] = water_values
  newdict["winter activities"] = winter_values
  newdict["cultural activities"] = cultural_values
  #activity_type_df = pd.DataFrame.from_dict(newdict, orient = 'index')
  #activity_type_df = activity_type_df.transpose()
  return activities, newdict



def getcampsitedata(campground_id):
  headers = {'Content-type': 'application/json', "apikey": "f5e1e19c-fb0f-4585-b080-09b688d535eb"} 
  r = requests.get(f'https://ridb.recreation.gov/api/v1/facilities/{campground_id}/campsites?limit=10&offset=0', headers = headers)
  data = r.json()
  
  site_types = []
  amenity_list = set()
  additional_features = set()
  regulations = set()
  reservable = False
  pet_friendly = False
  ada_accessible = False
  
  for thing in data["RECDATA"]:
    for attribute in thing["ATTRIBUTES"]:
          if attribute == {'AttributeName': 'Picnic Table', 'AttributeValue': 'Y'}:
            amenity_list.add("picnic tables")
          if attribute == {'AttributeName': 'CAMPFIRE RINGS', 'AttributeValue': 'Campfire Rings'} or attribute == {'AttributeName': 'Fire Pit', 'AttributeValue': 'Y'}:
            amenity_list.add("fire rings")
          if attribute == {'AttributeName': 'FOOD STORAGE LOCKER', 'AttributeValue': 'Food Storage Locker'}:
            amenity_list.add("food storage lockers")
          if attribute == {'AttributeName': 'Pets Allowed', 'AttributeValue': 'Yes'}:
            pet_friendly = True
    if thing['CampsiteType'] != 'MANAGEMENT':
      site_types.append(thing['CampsiteType'])
    if thing["CampsiteAccessible"] == "TRUE":
              ada_accessible = True
  
    if thing["CampsiteReservable"] == "TRUE":
              reservable = True

  num_of_sites = len(site_types)
  site_types = set(site_types)
  #print(num_of_sites, site_types, amenity_list)
  return num_of_sites, site_types, amenity_list

def sorted_activities():
    headers = {'Content-type': 'application/json', "apikey": "********************"} 
    r = requests.get('https://ridb.recreation.gov/api/v1/activities?limit=300&offset=0', headers = headers)
    data = r.json()

    activities_dict = {}
    winter_values = []
    summer_values = []
    water_values = []
    cultural_values = []
    water_activities_list = ["boating", "fishing", "water sports", "swimming site", "paddling", "swimming", "diving", "snorkeling", "paddle boating", "water activities", "kayaking", "canoeing", "sea kayaking", "surfing", "jet skiing", "water skiing", "water access", "non-motorized boating", "windsurfing", "rafting", "whitewater rafting", "river trips", "sailing", "scuba diving", "accessible swimming", "boat rental"]
    winter_activities_list = ["winter sports", "snowpark", "snowmobile", "ice climbing", "ice fishing", "snowmobiling", "sledding", "skiing", "downhill skiing", "snowboarding", "ice fishing", "ice skating", "snow tubing", "snowmobile trails"]
    cultural_activities_list = ["historical and cultural site", "interpretive programs", "documentary site", "information site", "environmental education", "information site", "cultural activites", "evening programs", "guided interpretive walks", "recreation programs", "educational programs", "historical sites", "museum"]
    for activity in data["RECDATA"]:
        if activity["ActivityName"].lower() in winter_activities_list:
            winter_values.append(activity["ActivityName"].lower())
        activities_dict["winter activity"] = winter_values
        if activity["ActivityName"].lower() in water_activities_list:
            water_values.append(activity["ActivityName"].lower())
        activities_dict["water activity"] = water_values
        if activity["ActivityName"].lower() in cultural_activities_list:
            cultural_values.append(activity["ActivityName"].lower())
        activities_dict["cultural activity"] = cultural_values
    #print(activities_dict)
    return activities_dict

def get_facilites_by_rec_area(area_id):
  headers = {'Content-type': 'application/json', "apikey": "***********************"} 
  r = requests.get(f'https://ridb.recreation.gov/api/v1/recareas/{area_id}/facilities?limit=1000&offset=0', headers = headers)
  data = r.json()
  for thing in data["RECDATA"]:
    if thing["FacilityTypeDescription"] != "Campground":
        continue

    reservable = False
    ada_accessible = False
    camp_name = thing["FacilityName"]
    if thing["Reservable"] == True:
      reservable = True
    if thing["FacilityAdaAccess"] == True:
      ada_accessible = True  
    campground_id = thing["FacilityID"]
    #print(camp_name + " reservable = " + f'{reservable}')

    num_of_sites, campsite_types, campsite_amenities = getcampsitedata(campground_id)
    camp_activities, activities_dict = getcampactivities(campground_id)
    winter_string = ""
    water_string = ""
    culture_string = ""

    for k in activities_dict:
      if len(activities_dict[k]) > 0:
        if k == "water activities":
          water_intro_string_list = ["Water-related activities include", "The area offers lots of water-related fun, such as", "Visitors can enjoy water-related activities such as"]
          water_string = (f"{water_intro_string_list[(random.randrange(len(water_intro_string_list)))]} {output_formatting_insert_and(activities_dict[k])}.")
          #print(water_string)
        if k == "winter activities":
          winter_intro_string_list = ["In the winter, the place is a popular destination for", "Winter activities available here include", "In winter time, visitors can enjoy"]
          winter_string = (f"{winter_intro_string_list[(random.randrange(len(winter_intro_string_list)))]} {output_formatting_insert_and(activities_dict[k])}.")
        if k == "cultural activities":
          culture_intro_string_list = ["Visitors can also enjoy cultural activities such as", "Visitors also have the chance to do cultural activities like", "Cultural activities are available too and include"]
          culture_string = (f"{culture_intro_string_list[(random.randrange(len(culture_intro_string_list)))]} {output_formatting_insert_and(activities_dict[k])}.")

    
    #DESCRIPTION
    print(f'{camp_name} is a developed camground in [RecAreaName]. {water_string} {winter_string} {culture_string}')
    #FACILITIES AND SERVICES
    if reservable == True:
      if 'TENT ONLY NONELECTRIC' in campsite_types and 'STANDARD NONELECTRIC' in campsite_types:
        print(f'{camp_name} has {num_of_sites} reservable tent and RV sites equipped with {output_formatting_insert_and(campsite_amenities)}.')
    #print(num_of_sites, campsite_types, campsite_amenities, camp_activities)
  return num_of_sites, campsite_types, campsite_amenities, camp_activities

def output_formatting_insert_and(myset):
  if len(myset) == 2:
    mylist = list(myset)
    mystring1 = ', '.join(mylist[0:-1])
    mystring2 = mystring1 + ' and ' + mylist[-1]
    return mystring2
  if len(myset) >= 2:
    mylist = list(myset)
    mystring1 = ', '.join(mylist[0:-1])
    mystring2 = mystring1 + ', and ' + mylist[-1] 
    return mystring2
  if len(myset) ==1:
    mystring = ', '.join(myset)
    return mystring



    
area_id = 2907
#2907 Rocky Mountain
get_facilites_by_rec_area(area_id)

#getcampsitedata(232463)
