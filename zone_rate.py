import json
import requests
import csv

zone_rate_dict={}

high_rate = 4
for Location_id, restaurants in zone_restaurant_dict.items():
	# print(len(restaurants))
	
	if len(restaurants)==0:
		print('There are no restaurants in',taxizone_dict[Location_id], 'zone')
		zone_rate_dict[Location_id] = 0
		zone_rate_dict[Location_id] = {'Average rating':0,'High rating(>4) restaurants':0,'Restaurants number':0,'High rating ratio':0}
		continue
	sum_rating = 0
	num_rating = 0
	num_high_rate=0
	for restaurant in restaurants:
		# print(restaurant['name'],restaurant['rating'])
		rate = float(restaurant['rating'])
		sum_rating += rate
		num_rating += 1
		if rate>=high_rate:
			num_high_rate += 1
	avg_rating = sum_rating/num_rating
	high_rate_ratio = num_high_rate/num_rating
	# print('There are',num_rating,'restaurants in',taxizone_dict[Location_id],'zone, and the average rating is',avg_rating,' Ratings higher than',high_rate,'is',high_rate_ratio)
	zone_rate_dict[Location_id] = {'Average rating':avg_rating,'High rating(>4) restaurants':num_high_rate,'Restaurants number':num_rating,'High rating ratio':high_rate_ratio}

filename = 'zone_rate_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(zone_rate_dict, outfile)

'''
filename = 'zone_rate_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_rate_dict = json.load(json_file)
# print(zone_rate_dict['1']['High rating(>4) restaurants'])
# print(zone_rate_dict.items())
# for item in zone_rate_dict.items():
# 	print(item[1])
zone_rate_sort_dict = {k: v for k, v in sorted(zone_rate_dict.items(),key=lambda x: int(x[1]['High rating(>4) restaurants']),reverse=True)}
# [1]['High rating(>4) restaurants']
# zone_rate_sort_dict = {k: v for k, v in sorted(zone_rate_dict.items(), key=lambda item: item['num_high_rate'])}
# sorted(zone_rate_dict,key=lambda x: x)
top_10_zone = list(zone_rate_sort_dict.items())[:6]
print(top_10_zone)

