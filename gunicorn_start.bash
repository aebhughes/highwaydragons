#!/bin/bash
 
NAME="highwaydragons"
FLASKDIR=/srv/highwaydragons
VIRTENV=/py3env
SOCKFILE=/srv/highwaydragons/run/gunicorn.sock
USER=root
GROUP=root
NUM_WORKERS=1
 
echo "Starting $NAME"
 
# Activate the virtual environment
cd $VIRTENV 
source bin/activate
export COUCHUSER=alex
export COUCHPW=fr3dalex
export UPLOADS=/srv/uploads/hwdragons

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
 
# Start your Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn $NAME:app -b 127.0.0.1:7100 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE
