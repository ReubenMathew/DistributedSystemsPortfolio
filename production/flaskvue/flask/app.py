from flask import Flask, render_template, jsonify
from flask_cors import CORS 
import requests
import redis

app = Flask(__name__,
			static_folder = './../dist/static',
			template_folder = './../dist')
cors = CORS(app, resources={r'/api/*': {'origins':'*'}})

app.config.from_object('config')

r = redis.Redis(host='192.168.99.100', port=6379, db=0)

@app.route('/api/spotify')
def db_call():
	api = {}
	# for x in r.keys():
	# 	if x[0:2] != b'rq':
	# 		api[x[1:]] == r.get(str(x[1:]))
	api['curr'] = r.get('curr').decode("utf-8")
	# api['prev'] = r.get('prev').decode("utf-8")
	
	return jsonify(api)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
