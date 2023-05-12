import requests
import json
import pandas as pd

#we query 3000 campsites to make sure we get all possible attributes
headers = {'Content-type': 'application/json', "apikey": "f5e1e19c-fb0f-4585-b080-09b688d535eb"} 
r = requests.get(f'https://ridb.recreation.gov/api/v1/campsites?limit=1000&offset=0', headers = headers)
data1 = r.json() #store result as json str

r = requests.get(f'https://ridb.recreation.gov/api/v1/campsites?limit=1000&offset=999', headers = headers)
data2 = r.json()  #store result as json str

r = requests.get(f'https://ridb.recreation.gov/api/v1/campsites?limit=1000&offset=1999', headers = headers)
data3 = r.json()  #store result as json str

data = merge(data1, data2, data3) #we merge the results of the above 3 queries into a single json string

attr_list = []
attr_set = set()
d = {}

def attrib_sort(camptype): #writes all unique attributes into a dict shaped as follows: {attribute : [value, value, value]}, filtered by CAMPSITE TYPE
    for thing in data["RECDATA"]:
        if camptype in thing["CampsiteType"]:
            for attribute in thing["ATTRIBUTES"]:
                a_name = attribute['AttributeName']
                a_value = attribute['AttributeValue']
            # if name not in dict add to dict set with value
                if a_name not in d.keys():
                  d[a_name] = [a_value]
                else: 
                 if a_value not in d[a_name]:
                     d[a_name].append(a_value)

    json_object = json.dumps(d, indent=4) #throw dict into json
 
    with open(f"All_{camptype}_Camp_Attributes.json", "w") as outfile:
        outfile.write(json_object) #and write it into a file

camptype = "EQUESTRIAN"
attrib_sort(camptype)
