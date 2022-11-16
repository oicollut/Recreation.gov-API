import requests
import json
import pandas as pd
headers = {'Content-type': 'application/json', "apikey": "f5e1e19c-fb0f-4585-b080-09b688d535eb"} 
r = requests.get('https://ridb.recreation.gov/api/v1/recareas/2988/facilities?limit=200&offset=0', headers = headers)
#Request URLs
#Rec areas: https://ridb.recreation.gov/api/v1/recareas?limit=50&offset=0
#Facilities: https://ridb.recreation.gov/api/v1/facilities?limit=10&offset=0
#all facilities of a rec area https://ridb.recreation.gov/api/v1/recareas/2907/facilities?limit=1000&offset=0
#all campsites of a facility https://ridb.recreation.gov/api/v1/facilities/233742/campsites?limit=50&offset=0
#all addresses of a facility https://ridb.recreation.gov/api/v1/facilities/259196/facilityaddresses?limit=50&offset=0
#all activities for a facility https://ridb.recreation.gov/api/v1/facilities/233742/activities?limit=50&offset=0



data = r.json()

#write_data = json.dumps(data, indent=4)
#print(write_data)

#with open("10_facilities.json", "w") as outfile:
#    outfile.write(write_data)



df_json = pd.json_normalize(data["RECDATA"])
df_json.to_excel("YellowstoneNP200Facilites.xlsx")


