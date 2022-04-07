import json
import requests
import csv

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