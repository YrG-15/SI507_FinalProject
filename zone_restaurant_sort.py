import json
import requests
import csv

filename = 'zone_restaurant_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_restaurant_dict = json.load(json_file)

zone_restaurant_sorted_dict = {}  #{locationID: restaurant sorted dict list high rating-low rating}
for zone,restaurants in zone_restaurant_dict.items():
	print(zone,len(restaurants))
	sort_restaurants = sorted(restaurants,key=lambda item: float(item['rating']),reverse=True)
	zone_restaurant_sorted_dict[zone] = sort_restaurants
	# break
# print(zone_restaurant_sorted_dict)

filename = 'zone_restaurant_sorted_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(zone_restaurant_sorted_dict, outfile)


filename = 'zone_restaurant_sorted_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_restaurant_sorted_dict = json.load(json_file)
# print(zone_restaurant_sorted_dict['1'])