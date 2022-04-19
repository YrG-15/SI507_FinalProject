import json
import requests
import csv
from secret import Yelpkey

#Get zones and their location ID-----------------------------------------------------------------------------------
folder = './archive/'
jsonfolder = './json_file/'
taxizone_filename = 'taxi+_zone_lookup.csv'

taxizone_dict = {} # {locationID: zone name}

with open(folder+taxizone_filename, newline='') as csvfile:
	zones = csv.reader(csvfile, delimiter='|')
	for row in zones:
		row[0] = row[0].replace('"', '')
		line = row[0].split(',')
		# line = line.strip('"')
		if line[0]=='LocationID':
			continue
		taxizone_dict[line[0]] = str(line[2])

# print(taxizone_dict)    # {locationID: zone name}
filename = 'taxizone_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(taxizone_dict, outfile)

filename = 'taxizone_dict.json'
with open(jsonfolder+filename) as json_file:
	taxizone_dict = json.load(json_file)
#Get restaurants in each zone-----------------------------------------------------------------------------------

zone_restaurant_dict = {} # {locationID: restaurant dict list}

filename = 'zone_restaurant_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_restaurant_dict = json.load(json_file)
print(zone_restaurant_dict)

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



filename = 'zone_restaurant_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_restaurant_dict = json.load(json_file)
# print(zone_restaurant_dict)
#calculate the ratings in each zone--------------------------------------------------------------------------------------------------------------------

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

#sort the restaurants in each zone--------------------------------------------------------------------------------------------------------------------

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

#taxi zone trip data--------------------------------------------------------------------------------------------------------------------

folder = './archive/'
taxitrip_filename = 'yellow_tripdata_2019-01.csv'

taxi_trip_lunch_PU_dict = {} # {locationID: PU num}
taxi_trip_lunch_DO_dict = {} # {locationID: DO num}
taxi_trip_dinner_PU_dict = {} # {locationID: PU num}
taxi_trip_dinner_DO_dict = {} # {locationID: DO num


with open(folder+taxitrip_filename, newline='') as csvfile:
	trips = csv.reader(csvfile, delimiter='|')
	for row in trips:
		# print(row)
		row[0] = row[0].replace('"', '')
		line = row[0].split(',')
		if line[0]=='VendorID':
			continue
		if int(line[1][11:13])<14 and int(line[1][11:13])>11 and line[7]!=line[8]:
			if line[7] in taxi_trip_lunch_PU_dict.keys():
				taxi_trip_lunch_PU_dict[line[7]] += 1
			else:
				taxi_trip_lunch_PU_dict[line[7]] = 1

			if line[8] in taxi_trip_lunch_DO_dict.keys():
				taxi_trip_lunch_DO_dict[line[8]] += 1
			else:
				taxi_trip_lunch_DO_dict[line[8]] = 1

		if int(line[1][11:13])<20 and int(line[1][11:13])>17 and line[7]!=line[8]:
			if line[7] in taxi_trip_dinner_PU_dict.keys():
				taxi_trip_dinner_PU_dict[line[7]] += 1
			else:
				taxi_trip_dinner_PU_dict[line[7]] = 1

			if line[8] in taxi_trip_dinner_DO_dict.keys():
				taxi_trip_dinner_DO_dict[line[8]] += 1
			else:
				taxi_trip_dinner_DO_dict[line[8]] = 1


taxi_trip_lunch_PU_dict = {k: v for k, v in sorted(taxi_trip_lunch_PU_dict.items(), key=lambda item: item[1],reverse=True)}
taxi_trip_lunch_DO_dict = {k: v for k, v in sorted(taxi_trip_lunch_DO_dict.items(), key=lambda item: item[1],reverse=True)}

taxi_trip_dinner_PU_dict = {k: v for k, v in sorted(taxi_trip_dinner_PU_dict.items(), key=lambda item: item[1],reverse=True)}
taxi_trip_dinner_DO_dict = {k: v for k, v in sorted(taxi_trip_dinner_DO_dict.items(), key=lambda item: item[1],reverse=True)}


filename = 'taxi_trip_lunch_PU_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(taxi_trip_lunch_PU_dict, outfile)

filename = 'taxi_trip_lunch_DO_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(taxi_trip_lunch_DO_dict, outfile)


filename = 'taxi_trip_dinner_PU_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(taxi_trip_dinner_PU_dict, outfile)

filename = 'taxi_trip_dinner_DO_dict.json'
with open(jsonfolder+filename, "w") as outfile:
	json.dump(taxi_trip_dinner_DO_dict, outfile)


# filename = 'taxi_trip_lunch_PU_dict.json'
# with open(jsonfolder+filename) as json_file:
# 	taxi_trip_lunch_PU_dict = json.load(json_file)

# filename = 'taxi_trip_lunch_DO_dict.json'
# with open(jsonfolder+filename) as json_file:
# 	taxi_trip_lunch_DO_dict = json.load(json_file)

# filename = 'taxi_trip_dinner_PU_dict.json'
# with open(jsonfolder+filename) as json_file:
# 	taxi_trip_dinner_PU_dict = json.load(json_file)
# filename = 'taxi_trip_dinner_DO_dict.json'
# with open(jsonfolder+filename) as json_file:
# 	taxi_trip_dinner_DO_dict = json.load(json_file)


# print(taxi_trip_lunch_DO_dict)
# taxi_trip_lunch_DO_dict_key = list(taxi_trip_lunch_DO_dict.keys())
# for i in range(10):
# 	print(taxi_trip_lunch_DO_dict_key[i],zone_rate_dict[taxi_trip_lunch_DO_dict_key[i]])


# print('dinner')
# taxi_trip_dinner_DO_dict_key = list(taxi_trip_dinner_DO_dict.keys())
# for i in range(10):
# 	print(taxi_trip_dinner_DO_dict_key[i],zone_rate_dict[taxi_trip_dinner_DO_dict_key[i]])



