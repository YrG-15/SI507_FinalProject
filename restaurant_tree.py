import json
import requests
import csv
from flask import Flask,render_template
import requests


app = Flask(__name__)


folder = './archive/'
jsonfolder = './json_file/'

filename = 'zone_restaurant_sorted_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_restaurant_sorted_dict = json.load(json_file)

filename = 'taxizone_dict.json'
with open(jsonfolder+filename) as json_file:
	taxizone_dict = json.load(json_file)

filename = 'zone_rate_dict.json'
with open(jsonfolder+filename) as json_file:
	zone_rate_dict = json.load(json_file)
zone_rate_sort_dict = {k: v for k, v in sorted(zone_rate_dict.items(),key=lambda x: int(x[1]['High rating(>4) restaurants']),reverse=True)}

top_10_zone = list(zone_rate_sort_dict.items())
# print(top_10_zone[2-1][0])

LeafTree = \
	("Do you want to get details of a specific restaurants?",
		"Which one do you like to get?",None)

Tree3 = \
	("Do you want to get the top 10 restaurants in this zone?",
		LeafTree,
		("How many top restaurants do you want to get?",LeafTree))

Tree2_top5 = \
	("Which zone do you like to search?(Type 1-5)",Tree3)

Tree2_top10 = \
	("Which zone do you like to search?(Type 1-10)",Tree3)

Tree2_zone = \
	("Which zone do you like to search?(Type Location ID)",Tree3)


RootTree = \
	("Do you want to search for restaurants in the zone with top 5 number of high rating restaurants?",
		Tree2_top5,
		("Do you want to search for restaurants in the zone with top 10 number of high rating restaurants?",Tree2_top10,Tree2_zone))

def playleaf(subsubsubtree,top_num,zone_N,flag):
	print(subsubsubtree[0])
	prompt = input()
	if yes(prompt):
		print(subsubsubtree[1])
		restaurant = int(input())
		detail = printdetail(zone_N,flag,restaurant)
	else:
		print("Quit")
		detail = 'Quit'
	return detail

def playsubsub(subsubtree,zone_N,flag):
	print(subsubtree[0])
	prompt = input()
	if yes(prompt):
		restaurant_list,restaurant_link_list,zone_name = printrestaurant(zone_N,flag,10)
		top_num = 10
	else:
		print(subsubtree[2][0])
		top_num = int(input())
		restaurant_list,restaurant_link_list,zone_name = printrestaurant(zone_N,flag,top_num)
	subsubsubtree = subsubtree[1]
	return subsubsubtree,top_num,restaurant_list,restaurant_link_list,zone_name

def playsub(subtree,flag):
	print(subtree[0])
	prompt = input()
	if flag==1 or flag==0:
		N= int(prompt)
	else:
		N = prompt
	subsubtree = subtree[1]
	return subsubtree,N

def playroot(RootTree):
	print(RootTree[0])
	prompt = input()
	if yes(prompt):
		subtree = RootTree[1]
		flag=0 					#top5
		printzones(flag)
	else:
		print(RootTree[2][0])
		prompt2 = input()
		if yes(prompt2):
			subtree = RootTree[2][1]
			flag=1 				#top10
			printzones(flag)
		else:
			subtree = RootTree[2][2]
			flag=2 				#location ID

	subsubtree,zone_N = playsub(subtree,flag)
	subsubsubtree,top_num,restaurant_list,restaurant_link_list,zone_name = playsubsub(subsubtree,zone_N,flag)
	detail = playleaf(subsubsubtree,top_num,zone_N,flag)
	print('')
	print('If you would like to get details of other top restaurants in',zone_name, '. Go to http://127.0.0.1:5000/restaurants/<your name>')
	print('')
	save_answer = input('Would you like to save this tree?')
	if yes(save_answer):
		newtree_filename = input('Please enter a file name:')
		print(newtree_filename)
		treefile = open(newtree_filename, "w")
		saveTree(RootTree,subtree,zone_name,subsubtree,top_num,subsubsubtree,detail,treefile)
		treefile.close()
		print('Thank you! The file has been saved.')
	return restaurant_list,top_num,restaurant_link_list,zone_name

def printzones(flag):
	if flag==0:
		for i in range(5):
			print(i+1,taxizone_dict[top_10_zone[i][0]])
	if flag==1:
		for i in range(10):
			print(i+1,taxizone_dict[top_10_zone[i][0]])

def printrestaurant(zone_N,flag,top_num):
	restaurant_list = []
	restaurant_link_list = []
	if flag==2:
		# print(zone_N)
		for i in range(top_num):
			print(i+1,zone_restaurant_sorted_dict[zone_N][i]['name'])
			restaurant_list.append(zone_restaurant_sorted_dict[zone_N][i]['name'])
			restaurant_link_list.append(zone_restaurant_sorted_dict[zone_N][i]['url'])
			zone_name = taxizone_dict[zone_N]
	else:
		for i in range(top_num):
			print(i+1,zone_restaurant_sorted_dict[top_10_zone[zone_N-1][0]][i]['name'])
			restaurant_list.append(zone_restaurant_sorted_dict[top_10_zone[zone_N-1][0]][i]['name'])
			restaurant_link_list.append(zone_restaurant_sorted_dict[top_10_zone[zone_N-1][0]][i]['url'])
			zone_name = taxizone_dict[top_10_zone[zone_N-1][0]]
	return restaurant_list,restaurant_link_list,zone_name

def printdetail(zone_N,flag,restaurant):
	if flag==2:
		# print(zone_restaurant_sorted_dict[zone_N][restaurant-1])
		detail = zone_restaurant_sorted_dict[zone_N][restaurant-1]
		for k,v in detail.items():
			print(k,':',v)
		return zone_restaurant_sorted_dict[zone_N][restaurant-1]
	else:
		# print(zone_restaurant_sorted_dict[top_10_zone[zone_N-1][0]][restaurant-1])
		detail = zone_restaurant_sorted_dict[top_10_zone[zone_N-1][0]][restaurant-1]
		for k,v in detail.items():
			print(k,':',v)
		return zone_restaurant_sorted_dict[top_10_zone[zone_N-1][0]][restaurant-1]

def yes(prompt):
    '''check whether the input is yes or no
    Parameters
    ----------
    prompt: string
        the input
    Returns
    -------
    answer: bool
        return True if input is yes or other fun options
        otherwise return False
    '''
    if prompt=='yes' or prompt=='y' or prompt=='yup' or prompt=='sure' :
        return True
    elif prompt=='no' or prompt=='n' :
        return False
    else:
        new_prompt = input("Please input yes or no.")
        return yes(new_prompt)

def saveTree(RootTree,subtree,zone_name,subsubtree,top_num,subsubsubtree,detail,treefile):
	print(RootTree[0],file=treefile)
	print(subtree[0],file=treefile)
	print('Answer:',file=treefile)
	print(zone_name,file=treefile)
	print(subsubtree[0],file=treefile)
	if top_num==10:
		print('Yes',file=treefile)
	else:
		print('No, Top restaurants Number:',top_num,file=treefile)
	print(subsubsubtree[0],file=treefile)
	if detail!='Quit':
		print('Yes, the detail of the restaurant is:',file=treefile)
		for k,v in detail.items():
			print(k,':',v, file=treefile)
	else:
		print('No')



def isleaf(tree):
	if type(tree[1]) is not tuple:
		return True
	else:
		return False

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/restaurants/<nm>')
def getheadlines(nm):
	restaurant_list,top_num,restaurant_link_list,zone_name = playroot(RootTree)
	return render_template('headlines_link.html',name=nm,headlines=restaurant_list,top_num=top_num,urls=restaurant_link_list,zone_name=zone_name)

if __name__ == '__main__':
	print('starting Flask app',app.name,'Please go to http://127.0.0.1:5000/restaurants/<your name> to start to get the restaurants')
	# restaurant_list,top_num,restaurant_link_list = playroot(RootTree)
	app.run(debug=True)




