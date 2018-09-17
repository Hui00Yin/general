import os
import requests
import operator
import re
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from mt_threads import * 

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def get_counts():
    # get url
    data = json.loads(request.data.decode())
    url = data["url"]
    if 'http' not in url[:4]:
        url = 'http://' + url
    print("get_counts: url is --->{}".format(url))
    return 


@app.route("/results", methods=['GET'])
def get_results():
    now = datetime.now()
    pickup_actions_time = now - timedelta(days=3)
    results = Results.query.filter(Results.time > pickup_actions_time).all()
    return str(results), 200


if __name__ == '__main__':
    try:
        monitor = ChangeMonitor('/tmp/testContent')
#        monitor.add_copy_imgs_job()
#        monitor.add_since_request_job()
        #monitor.start()

        app.run(host='0.0.0.0')
    except (KeyboardInterrupt, SystemExit):
        print("Shutdown monitor!")
        monitor.shutdown()
