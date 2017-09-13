# Replicating CouchDB to Remote Server

    from couchdb import Server

    # Connect without any admin permissions
    local_server = Server() 

    # Connect with Admin permissions
    local_server = Server(http://aebhughes:fr3dalex@localhost:5984')

    # Connect with Admin permissions
    remote_server = Server('http://aebhughes:fr3dalex@178.62.83.205:5984')

    local_db = local_server['db_name']
    
    local_db = local_server.create('db_name')

    there_db = remote_server['db_name']

    there_db = remote_server.create('db_name')

    local_URL = 'http://localhost:5984'
    remote_URL = 'http://178.62.83.205:5984'

    source = '/'.join([local_URL,'db_name'])
    dest = '/'.join([remote_URL,'db_name'])

    local_server.replicate(source, dest)

Carries over attachments like a dream....
Quite swift, as well.

returns:
    {'ok': True, 
     'replication_id_version': 3, 
     'history': [
                 {
                  'recorded_seq': 3, 
                  'start_time': 'Mon, 26 Sep 2016 12:43:21 GMT', 
                  'end_time': 'Mon, 26 Sep 2016 12:43:24 GMT', 
                  'docs_read': 1, 
                  'docs_written': 1, 
                  'start_last_seq': 0, 
                  'missing_checked': 1, 
                  'missing_found': 1, 
                  'doc_write_failures': 0, 
                  'session_id': 'ef196c06d20d90262a8dc5949f66b6da', 
                  'end_last_seq': 3}
                ], 
     'session_id': 'ef196c06d20d90262a8dc5949f66b6da', 
     'source_last_seq': 3}


