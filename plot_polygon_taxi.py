import json
import requests
import csv
from secret import Yelpkey
import matplotlib.pyplot as plt 
import matplotlib 
from matplotlib.patches import Polygon
from matplotlib.path import Path 
import re
import matplotlib.patches as mpatches

folder = './archive/'
jsonfolder = './json_file/'


filename = 'taxi_trip_lunch_PU_dict.json'
with open(jsonfolder+filename) as json_file:
	taxi_trip_lunch_PU_dict = json.load(json_file)

filename = 'taxi_trip_lunch_DO_dict.json'
with open(jsonfolder+filename) as json_file:
	taxi_trip_lunch_DO_dict = json.load(json_file)

print(taxi_trip_lunch_DO_dict.keys())

filename = 'taxi_trip_dinner_PU_dict.json'
with open(jsonfolder+filename) as json_file:
	taxi_trip_dinner_PU_dict = json.load(json_file)
filename = 'taxi_trip_dinner_DO_dict.json'
with open(jsonfolder+filename) as json_file:
	taxi_trip_dinner_DO_dict = json.load(json_file)

filename = 'taxi_zone.json'
with open(jsonfolder+filename) as json_file:
	taxi_zone = json.load(json_file)




def polycolor_taxi_lunch(lunch_DO):
	if lunch_DO>=25000:
		lunch_color = 'gold'
	elif lunch_DO<25000 and lunch_DO>=20000:
		lunch_color = 'orange'
	elif lunch_DO<20000 and lunch_DO>=15000:
		lunch_color = 'deepskyblue'
	elif lunch_DO<15000 and lunch_DO>=10000:
		lunch_color = 'lightskyblue'
	elif lunch_DO<10000 and lunch_DO>=5000:
		lunch_color = 'forestgreen'
	elif lunch_DO<5000 and lunch_DO>=3000:
		lunch_color = 'springgreen'
	elif lunch_DO<3000 and lunch_DO>=1000:
		lunch_color = 'seagreen'
	elif lunch_DO<1000 and lunch_DO>=500:
		lunch_color = 'paleturquoise'
	elif lunch_DO<500 and lunch_DO>=250:
		lunch_color = 'lawngreen'
	else:
		lunch_color = 'darkgreen'
	return lunch_color

def polycolor_taxi_dinner(dinner_DO):
	if dinner_DO>=25000:
		dinner_color = 'red'
	elif dinner_DO<25000 and dinner_DO>=20000:
		dinner_color = 'black'
	elif dinner_DO<20000 and dinner_DO>=10000:
		dinner_color = 'darkviolet'
	elif dinner_DO<10000 and dinner_DO>=5000:
		dinner_color = 'blue'
	elif dinner_DO<5000 and dinner_DO>=3000:
		dinner_color = 'mediumpurple'
	elif dinner_DO<3000 and dinner_DO>=1000:
		dinner_color = 'mediumorchid'
	elif dinner_DO<1000 and dinner_DO>=500:
		dinner_color = 'deeppink'
	elif dinner_DO<500 and dinner_DO>=250:
		dinner_color = 'blueviolet'
	else:
		dinner_color = 'orchid'
	return dinner_color

class NYU_Zone:
	def __init__(self,coordinates,name,ID,\
		lunch_DO,dinner_DO,lunch_color,dinner_color):
		self.Coordinates = coordinates
		self.name = name
		self.ID = ID
		self.lunch_DO = lunch_DO
		self.dinner_DO = dinner_DO
		self.lunch_color = lunch_color
		self.dinner_color = dinner_color

zone_num = len(taxi_zone['data'])
NYU_Zone_list = []
for i in range(zone_num):
	coordinates_string = taxi_zone['data'][i][-5][12:-3]
	coordinates_list = coordinates_string.split(',')
	coordinates = []
	for coordinate in coordinates_list:
		new_coordinates = coordinate[1:].split(' ')
		for j in range(len(new_coordinates)):
			new_coordinates[j] = new_coordinates[j].strip('(')
			new_coordinates[j] = new_coordinates[j].strip(')')
			new_coordinates[j] = float(new_coordinates[j])
		coordinates.append(new_coordinates)
	# print(coordinates)
	ID = taxi_zone['data'][i][-2]
	name = taxi_zone['data'][i][-3]


	if ID in taxi_trip_lunch_DO_dict:
		lunch_DO = taxi_trip_lunch_DO_dict[ID]
	else:
		lunch_DO = 0

	if ID in taxi_trip_dinner_DO_dict:
		dinner_DO = taxi_trip_dinner_DO_dict[ID]
	else:
		dinner_DO = 0
	# print(ID,name,avg_rating,high_rating_ratio)

	lunch_color = polycolor_taxi_lunch(lunch_DO)
	dinner_color = polycolor_taxi_dinner(dinner_DO)

	print(name, ID)
	nyuzone = NYU_Zone(coordinates, name, ID,\
		lunch_DO, dinner_DO, lunch_color, dinner_color)
	NYU_Zone_list.append(nyuzone)


# print(NYU_Zone_list)
Zone_poly = [] 
for i in range(zone_num):
    polygon = Polygon(NYU_Zone_list[i].Coordinates, True)
    # print(DetroitDistrict["Holc_Color"][i])
    polygon.set_color(NYU_Zone_list[i].lunch_color)
    polygon.set_edgecolor(NYU_Zone_list[i].dinner_color)
    Zone_poly.append(polygon)

fig, ax = plt.subplots() 
for u in Zone_poly:      
	ax.add_patch(u) 
	ax.autoscale() 
plt.rcParams["figure.figsize"] = (15,15) 
plt.title('New York Taxi Zone according to taxi dropoff times')
A1_patch = mpatches.Patch(color='gold', label='Lunch Drop off times > 25000')
A2_patch = mpatches.Patch(color='orange', label='Lunch Drop off times > 20000')
B1_patch = mpatches.Patch(color='deepskyblue', label='Lunch Drop off times > 15000')
B2_patch = mpatches.Patch(color='lightskyblue', label='Lunch Drop off times > 10000')
C_patch = mpatches.Patch(color='forestgreen', label='Lunch Drop off times > 5000')
D_patch = mpatches.Patch(color='springgreen', label='Lunch Drop off times > 3000')
E_patch = mpatches.Patch(color='seagreen', label='Lunch Drop off times > 1000')
F_patch = mpatches.Patch(color='paleturquoise', label='Lunch Drop off times > 500')
G_patch = mpatches.Patch(color='lawngreen', label='Lunch Drop off times > 250')
H_patch = mpatches.Patch(color='darkgreen', label='Lunch Drop off times < 250')
A_edge = mpatches.Patch(edgecolor= 'red',facecolor='white',label='Dinner Drop off times > 25000')
B_edge = mpatches.Patch(edgecolor= 'black',facecolor='white',label='Dinner Drop off times > 20000')
C_edge = mpatches.Patch(edgecolor= 'darkviolet',facecolor='white',label='Dinner Drop off times > 10000')
D_edge = mpatches.Patch(edgecolor= 'blue',facecolor='white',label='Dinner Drop off times > 5000')
E_edge = mpatches.Patch(edgecolor= 'mediumpurple',facecolor='white',label='Dinner Drop off times > 3000')
F_edge = mpatches.Patch(edgecolor= 'mediumorchid',facecolor='white',label='Dinner Drop off times > 1000')
G_edge = mpatches.Patch(edgecolor= 'deeppink',facecolor='white',label='Dinner Drop off times > 500')
H_edge = mpatches.Patch(edgecolor= 'blueviolet',facecolor='white',label='Dinner Drop off times > 250')
I_edge = mpatches.Patch(edgecolor= 'orchid',facecolor='white',label='Dinner Drop off times < 250')



plt.legend(handles=[A1_patch,A2_patch,B1_patch,B2_patch,C_patch,D_patch,E_patch,F_patch,G_patch,H_patch,\
	A_edge,B_edge,C_edge,D_edge,E_edge,F_edge,G_edge,H_edge,I_edge],fontsize=4.3)

plt.show() 
