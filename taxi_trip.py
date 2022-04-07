
import json
import requests
import csv

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