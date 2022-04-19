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
filename = 'taxi_zone.json'

with open(jsonfolder+filename) as json_file:
	taxi_zone = json.load(json_file)

zone_rate_filename = 'zone_rate_dict.json'
with open(jsonfolder+zone_rate_filename) as json_file:
	zone_rate_dict = json.load(json_file)

def polycolor(avg_rating):
	if avg_rating>=4.5:
		avg_rating_Grade = 'A1'
		rating_color = 'gold'
	elif avg_rating<4.5 and avg_rating>=4:
		avg_rating_Grade = 'A2'
		rating_color = 'orange'
	elif avg_rating<4 and avg_rating>=3.5:
		avg_rating_Grade = 'B1'
		rating_color = 'deepskyblue'
	elif avg_rating<3.5 and avg_rating>=3:
		avg_rating_Grade = 'B2'
		rating_color = 'lightskyblue'
	elif avg_rating<3 and avg_rating>=2:
		avg_rating_Grade = 'C'
		rating_color = 'forestgreen'
	else:
		avg_rating_Grade = 'D'
		rating_color = 'darkgreen'
	return avg_rating_Grade,rating_color

def edgecolor(high_rating_ratio):
	if high_rating_ratio>=0.8:
		high_rating_color = 'red'
	elif high_rating_ratio<0.8 and high_rating_ratio>=0.6:
		high_rating_color = 'black'
	elif high_rating_ratio<0.6 and high_rating_ratio>=0.4:
		high_rating_color = 'darkviolet'
	elif high_rating_ratio<0.4and high_rating_ratio>=0.2:
		high_rating_color = 'blue'
	else:
		high_rating_color = 'lightseagreen'
	return high_rating_color

class NYU_Zone:
	def __init__(self,coordinates,avg_rating_Grade,rating_color,high_rating_ratio, high_rating_color,avg_rating, name,ID):
		self.Coordinates = coordinates
		self.avg_rating_Grade = avg_rating_Grade
		self.rating_color = rating_color
		self.high_rating_ratio = high_rating_ratio
		self.high_rating_color = high_rating_color
		self.avg_rating = avg_rating
		self.name = name
		self.ID = ID


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
	avg_rating = zone_rate_dict[ID]['Average rating']
	high_rating_ratio = zone_rate_dict[ID]['High rating ratio']
	# print(ID,name,avg_rating,high_rating_ratio)
	avg_rating_Grade,rating_color = polycolor(avg_rating)
	high_rating_color = edgecolor(high_rating_ratio)
	
	print(avg_rating_Grade,rating_color,high_rating_ratio,high_rating_color, avg_rating, name,ID)
	nyuzone = NYU_Zone(coordinates,avg_rating_Grade,rating_color,high_rating_ratio, high_rating_color, avg_rating, name,ID)
	NYU_Zone_list.append(nyuzone)


# print(NYU_Zone_list)
Zone_poly = [] 
for i in range(zone_num):
    polygon = Polygon(NYU_Zone_list[i].Coordinates, True)
    # print(DetroitDistrict["Holc_Color"][i])
    polygon.set_color(NYU_Zone_list[i].rating_color)
    polygon.set_edgecolor(NYU_Zone_list[i].high_rating_color)
    Zone_poly.append(polygon)



fig, ax = plt.subplots() 
for u in Zone_poly:      
	ax.add_patch(u) 
	ax.autoscale() 
plt.rcParams["figure.figsize"] = (15,15) 
plt.title('New York Taxi Zone according to Restaurants\' Rating')
A1_patch = mpatches.Patch(color='gold', label='Avgerage rating > 4.5')
A2_patch = mpatches.Patch(color='orange', label='Avgerage rating > 4')
B1_patch = mpatches.Patch(color='deepskyblue', label='Avgerage rating > 3.5')
B2_patch = mpatches.Patch(color='lightskyblue', label='Avgerage rating > 3')
C_patch = mpatches.Patch(color='forestgreen', label='Avgerage rating > 2')
D_patch = mpatches.Patch(color='darkgreen', label='Avgerage rating < 2')
A_edge = mpatches.Patch(edgecolor= 'red',facecolor='white',label='High rating ratio > 0.8')
B_edge = mpatches.Patch(edgecolor= 'black',facecolor='white',label='High rating ratio > 0.6')
C_edge = mpatches.Patch(edgecolor= 'darkviolet',facecolor='white',label='High rating ratio > 0.4')
D_edge = mpatches.Patch(edgecolor= 'blue',facecolor='white',label='High rating ratio > 0.2')
E_edge = mpatches.Patch(edgecolor= 'lightseagreen',facecolor='white',label='High rating ratio < 0.2')

plt.legend(handles=[A1_patch,A2_patch,B1_patch,B2_patch,C_patch,D_patch,A_edge,B_edge,C_edge,D_edge,E_edge],fontsize=7)

plt.show() 
