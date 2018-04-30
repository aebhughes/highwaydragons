#!/bin/bash
 
NAME="highwaydragons"
FLASKDIR=/var/www/HighwayDragons
SOCKFILE=/var/www/HighwayDragons/run/gunicorn.sock
USER=root
GROUP=root
NUM_WORKERS=1
 
echo "Starting $NAME"
 
# Activate the virtual environment
source /var/www/.env/bin/activate
export COUCHUSER=aebhughes
export COUCHPW='Custom Soft Her0!'
export UPLOADS=/srv/uploads

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
  --log-level=info \
  --bind=unix:$SOCKFILE
