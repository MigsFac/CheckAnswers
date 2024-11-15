from flask import Flask,session
from flask_session import Session
import redis
app = Flask(__name__)
app.config.from_object('mathg.config')

#app.config['SESSION_TYPE'] = 'redis'
#app.config['SESSION_PERMANENT'] = False
#app.config['SESSION_USE_SIGNER'] = True
#app.config['SESSION_KEY_PREFIX'] = 'flask_session:'
#app.config['SESSION_REDIS'] = redis.Redis(host='localhost',port=6379,db=0)
#Session(app)

import mathg.views
from mathg import db
db.create_Title()