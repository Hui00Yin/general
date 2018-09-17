import time
import logging
from datetime import datetime, timedelta
import os, sh,sys, traceback
from Queue import Queue,Empty
from threading import Thread
import requests
import json
from app import db
from flask_sqlalchemy import SQLAlchemy
from models import *

url = 'http://wtl-hmo-1:9005/storages/files/since/b4958a11-239a-40d4-97f0-bf5bc8fd24d6?limit=20000'
headers = {'Content-type': 'application/json'}

my_pwd = "W4terl00\n"
from apscheduler.schedulers.background import BackgroundScheduler

class ChangeMonitor:
    def __init__(self, path):
        self.path = path 
        self.q = Queue()
        self.scheduler = BackgroundScheduler()
        self.changes_queue = []
        self.rcv_thread = self.rcv_notify()
        self._running = True
        self.cooling_time = 30

    def rcv_notify(self):
        def rcv():
            while self._running:
                try:
                    name = self.q.get(timeout=1.0)
                    self.changes_queue.append(name)
                    self.q.task_done()
                    n,a = name.split(':')
                    actions = Actions(name = n.split('.')[0], action = a, time=datetime.now())
                    db.session.add(actions)
                    db.session.commit()
                except Empty:
                    pass
                except (KeyboardInterrupt, SystemExit):
                    print("No more receive messages!")
                    return
        return Thread(target=rcv)

    def start(self):
        self.rcv_thread.start()
        self.scheduler.start()

    def shutdown(self):
        self._running = False
        self.scheduler.shutdown()

    def create_name(self, path = '/tmp/testContent'):
        time1 = str(datetime.now())
        n = time1.split('.')[0]
        n = '_'.join(n.split(' '))
        n = '_'.join(n.split(':'))
        name = 'M%s.jpg' % n 
        return name, path + '/' + name

    def add_copy_imgs_job(self):
        def copy_images():
            try:
                my_sudo = sh.sudo.bake("-S", _in=my_pwd)
                files = [(os.path.join(self.path, f),f) for f in os.listdir(self.path)]

                length = len(files)
                if length > 500:
                    if self.cooling_time > 0:
                        self.cooling_time= self.cooling_time - 1
                    else:
                        cooling_time = 30;
                        for full_f, f in files:
                            my_sudo.rm(full_f)
                            self.q.put(f + ' :Filedeleted')
                else: 
                    name,full_name = self.create_name()
                    #print("cp files:%s" % name) 
                    my_sudo.cp('/tmp/TestMedia/jpg/MonaLisa1.jpg', full_name)
                    self.q.put(name + ' :Filemetadata')
            except Exception as e:
                print ("Error is {}".format(e))


        self.scheduler.add_job(copy_images, 'interval', seconds=10)
    
    def since_request(self):
        #r = requests.get(url, json=data, headers=headers)
        r = requests.get(url)
        changes = json.loads(r.text)
        return [(change["Name"], change["eventType"]) for change in changes["results"]]

    def add_since_request_job(self):
        def print_message():
            try:
                pickup_actions_time = datetime.now() - timedelta(minutes=3)
                actions = Actions.query.filter((Actions.time < pickup_actions_time) & (Actions.checked == False)).all()
                since_changes = self.since_request()
                changes = []
                for change in actions:
                    change.checked = True
                    matched = False
                    for name, action in since_changes:
                        if change.name == name and change.action == action:
                            matched = True
                            break
                    
                    if not matched:
                        result = Results(name = change.name, action = change.action, time = datetime.now())
                        db.session.add(result)
                        db.session.commit()
                        print("--->{} not been recorded!".format(change)) 

                db.session.commit()
                
            
            except Exception as e:
                print("The error is: {}".format(e))
                traceback.print_exc(file=sys.stdout)

        self.scheduler.add_job(print_message, 'interval', minutes=10)

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    monitor = ChangeMonitor('/tmp/testContent')
    monitor.add_copy_imgs_job()
    monitor.add_since_request_job()
    monitor.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        while True:
            time.sleep(60)
            print("I'm main thread, still running!")
    except (KeyboardInterrupt, SystemExit):
        print("Shutdown monitor!")
        monitor.shutdown()
