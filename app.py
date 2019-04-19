from flask import Flask, render_template, request, redirect, request, Response
import jinja2
import os
import json 

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
	pos = pos % 7
	return str(json_var[keys_arr[pos]]).encode("utf-8")

@app.route('/init', methods=['GET'])
def init():
	global pos
	pos = -1

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)