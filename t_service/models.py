from app import db
import json


class Actions(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    print("The id in action table is: {}".format(id))
    name = db.Column(db.String())
    action = db.Column(db.String())
    time = db.Column(db.DateTime())
    checked = db.Column(db.Boolean)

    def __init__(self, name, action, time):
        self.name = name
        self.action = action
        self.time = time
        self.checked = False

    def __repr__(self):
        return json.dumps({'No': self.id, 'name': self.name, 'action': self.action, 'time': str(self.time)})

class Results(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    print("The id in results table is: {}".format(id))
    name = db.Column(db.String())
    action = db.Column(db.String())
    time = db.Column(db.DateTime())

    def __init__(self, name, action, time):
        self.name = name
        self.action = action
        self.time = time

    def __repr__(self):
        return json.dumps({'No': self.id, 'name': self.name, 'action': self.action, 'time': str(self.time)})
