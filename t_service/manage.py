import os
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from mt_threads import * 

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

def start_server():
    monitor = ChangeMonitor('/tmp/testContent')
    monitor.add_copy_imgs_job()
    monitor.add_since_request_job()
    monitor.start()
    return Server(host="0.0.0.0")

manager.add_command("runserver", start_server())

if __name__ == '__main__':
    manager.run()
