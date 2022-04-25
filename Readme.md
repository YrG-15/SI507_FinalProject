Required package:
Flask, requests, matplotlib, csv, re, webbrowser

Get data:
If you want to get all the data, directly run Getdata.py.

If you want to get part of the data, follow the instruction below:
1. Run taxi_zone.py to get zones with their location ID and save it in a dictionary.
2. Add a file called secret.py and add Yelpkey='Your key' in the file. Run zone_retaurants.py to get restaurants in each zone
3. Run zone_rate.py to calculate the average ratings, amount of high rating(>4) restaurants and high rating ratio in each zone.
4. Run zone_restaurant_sort.py to sort the restaurants according to the ratings in each zone.
5. Run taxi_trip.py to get taxi zone trip data, calculate the most popular lunch and dinner zones.

All the saved dictionaries are in json_file folder and saved as json files, zone_restaurant_dict.json and zone_restaurant_sorted_dict.json are too big to upload.

Data processing(After getting all data):
1. Run plot_polygon_rating.py to get the colorful polygons of New York taxi zone according to the average rating or high rating in each zone.
2. Run plot_polygon_taxi.py to get the colorful polygons of New York taxi zone according to the lunch and dinner drop off times in each zone.

Data structure:
Ask user what zone and restaurant information they would like to get.

Run restaurant_tree.py.

User could choose whether to save the tree by typing the filename.
