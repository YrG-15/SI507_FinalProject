import json
import requests
import csv

zone_restaurant_dict = {} # {locationID: restaurant dict list}

filename = 'zone_restaurant_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_restaurant_dict = json.load(json_file)
print(zone_restaurant_dict)

Yelpkey = 'GHzWimFTc5wCCqOOX-f-8IOxhBO2zrdXFHasafLPhdn6Vi6g_jQi0ZD96J5rIX-vcdrPTwges2ZiJNgpShkZCOgE_XQDiIW8whAa4hjlQ21uRLpy3N25RprXfnBHYnYx'
headers = {'Authorization': 'Bearer %s' % Yelpkey}
url='https://api.yelp.com/v3/businesses/search'

key_list = ['name','rating','phone','image_url','url']


for Location_id,zone in taxizone_dict.items():
	print(Location_id, zone)
	zone_restaurant_dict[Location_id] = []
	params = {'term':'food','location':zone,'limit':50,'offset':10}
	req=requests.get(url, params=params, headers=headers)
	print(req.status_code)
	if req.status_code!=200:
		continue
	text = json.loads(req.text)
	totalnum = text['total']
	print('totalnum',totalnum)

	if totalnum<50:
		offsets = [totalnum]
	else:
		offsets = range(50,(int(totalnum/50)+1)*50,50)

	for offset in offsets:
		params = {'term':'food','location':zone,'limit':50,'offset':offset}
		req=requests.get(url, params=params, headers=headers)
		if req.status_code!=200:
			continue
		text = json.loads(req.text)
		# print(text)
		restaurants = text['businesses']
		
		for i in range(len(restaurants)):
			restaurant_dict_tmp = {}
			for key in key_list:
				restaurant_dict_tmp[key] = restaurants[i][key]
			restaurant_dict_tmp['location'] = restaurants[i]['location']['display_address']
			zone_restaurant_dict[Location_id] += [restaurant_dict_tmp]
	filename = 'zone_restaurant_dict.json'
	with open(jsonfolder+filename, "w") as outfile:
		json.dump(zone_restaurant_dict, outfile)
	print(len(zone_restaurant_dict[Location_id]))
print(zone_restaurant_dict) # {locationID: restaurant dict list}

filename = 'zone_restaurant_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(zone_restaurant_dict, outfile)
'''


filename = 'zone_restaurant_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_restaurant_dict = json.load(json_file)
# print(zone_restaurant_dict)