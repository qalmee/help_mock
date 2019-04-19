from flask import Flask, render_template, request, redirect, request, Response
import jinja2
import os
import questions
import json 
import answers
from movesfinder import MovesFinder

app = Flask(__name__)


#Read JSON data into the datastore variable
json_var = json.load(open("mock.json", 'r'))

#Use the new datastore datastructure

keys = json_var.keys()
keys_arr = []
for key in keys:
	keys_arr.append(key)
pos = -1


@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/change')
def chance():
	return redirect('/')

@app.route('/post', methods=['GET','POST'])
def post():
	if request.method == 'POST':
		return render_template('post.html')
	return render_template('get.html')

@app.route('/get_help', methods=['POST'])
def get_help():
	global pos
	global json_var
	global keys_arr
	pos = pos + 1
	return str(json_var[keys_arr[pos]]).encode("cp1251")

@app.route('/get_help_test', methods=['POST'])
def get_help_test():
	json = request.get_json()
	movesfinder = MovesFinder()
	match = questions.find_best_match(json["question"])
	possible_moves = []
	if match[0] == 0:
		possible_moves = movesfinder.get_list_moves(json["board"])
	elif match[0] == 1:
		possible_moves = movesfinder.how_best_move(json["board"])
	answer = "haha"	
	print(possible_moves)
	return ("123", "234")

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)