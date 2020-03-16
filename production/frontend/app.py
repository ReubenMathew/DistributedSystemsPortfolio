from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import requests
import redis

app = Flask(__name__,
			static_folder = './dist/static',
			template_folder = './dist')
cors = CORS(app, resources={r'/api/*': {'origins':'*'}})
app.config['CORS_HEADERS'] = 'Content-Type'


r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/api/spotify')
@cross_origin(origin='*',headers=['Content-Type'])
def db_call():
	api = {}
	try:
		r.get('curr')
		api['curr'] = r.get('curr').decode("utf-8")
	except redis.exceptions.ConnectionError:
		api['curr'] = 'NULL'

	# api['prev'] = r.get('prev').decode("utf-8")
	
	return jsonify(api)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin(origin='*',headers=['Content-Type'])
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
	app.run()
