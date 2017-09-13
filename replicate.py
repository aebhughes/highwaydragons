from couchdb import Server

local_server = Server() 

# Connect with Admin permissions
local_server = Server('http://aebhughes:fr3dalex@localhost:5984')

# Connect with Admin permissions
remote_server = Server('http://aebhughes:fr3dalex@178.62.83.205:5984')

local_db = local_server['highwaydragons']
    
there_db = remote_server.create('highwaydragons')

local_URL = 'http://localhost:5984'
remote_URL = 'http://178.62.83.205:5984'

source = '/'.join([local_URL,'highwaydragons'])
dest = '/'.join([remote_URL,'highwaydragons'])

local_server.replicate(source, dest)
