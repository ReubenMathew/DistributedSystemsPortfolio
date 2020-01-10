from flask_rq2 import RQ
from rq import get_current_job
import requests
import random
import simplejson
import json

# (production)
import redis
r = redis.Redis(host='redis', port=6379, db=0)

rq = RQ()
rq.redis_url = 'redis://redis:6379/0'

# from rq_scheduler import Scheduler
# from datetime import datetime
# scheduler = Scheduler(connection=Redis())

# scheduler.schedule(
#     scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
#     func=callSpotify,                     # Function to be queued
#     interval=60,                   # Time before the function is called again, in seconds
#     repeat=None,                     # Repeat this number of times (None means repeat forever
# )


# (development only) insert easydbio creds and instantiate object...

# db = easydbio.DB({
#   "database": "5741e0d0-68ab-447e-8488-24ca97755690",
#   "token": "70e331da-07d9-4259-917a-246232b3a26d"
# })

@rq.job(timeout=180)
def callSpotify():
    self_job = get_current_job()

    f = open('creds.csv', "r")
    creds = f.read().split("\n") # "\r\n" if needed
    creds = creds[0].split(',')

    CLIENT_ID = creds[0]
    CLIENT_SECRET = creds[1]

    grant_type = 'client_credentials'
    body_params = {'grant_type' : grant_type}

    url='https://accounts.spotify.com/api/token'
    response = requests.post(url, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET)) 

    token_raw = simplejson.loads(response.text)
    token = token_raw["access_token"]
    headers = {"Authorization": "Bearer {}".format(token)}
    req = requests.get(url="https://api.spotify.com/v1/playlists/6o37RoezJdsZgk4Yi6OWrD/tracks", headers=headers)
    tracks = json.loads(req.text)
    peep = tracks['items'][-1]['track']

    trackName = peep['name']
    artist = peep['artists'][-1]['name']

    prev = r.get('curr')
    if prev == None:
        r.set('previous','null')    
    else:
        r.set('previous',prev)
    curr = f'{trackName} by {artist}'
    r.set('curr',curr)

    # try:
    #     prev = db.Get('curr')
    # except:
    #     db.Put('curr','null')
    #     prev = db.Get('curr')
    # db.Put('previous',prev)
    # curr = f'{trackName} by {artist}'
    # db.Put('curr',curr)

    self_job.meta['progress'] = {'num_iterations': 1, 'iteration': 1, 'percent': 100}
    # save meta information to queue
    self_job.save_meta()

    return curr