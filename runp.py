from flask import Flask
from views import app

# import redis
# app = Flask(__name__)
app.config.from_object("config")

# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_KEY_PREFIX'] = 'flask_session:'
# app.config['SESSION_REDIS'] = redis.Redis(host='localhost',port=6379,db=0)
# Session(app)

import db

db.create_Title()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
