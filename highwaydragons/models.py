import os
from uuid import uuid4
from werkzeug.utils import secure_filename

from couchdb import Server
couch = Server()
couch.resource.credentials = (os.environ['COUCHUSER'],os.environ['COUCHPW'])
db = couch['highwaydragons']

class Club(object):
    def __init__(self, **kwargs):
        self.doc = None
        if 'key' in kwargs:
            self.doc = db.get(kwargs['key']) 
        

class Member(Club):
    def __init__(self, **kwargs):
        pass
