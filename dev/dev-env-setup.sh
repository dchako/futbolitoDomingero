#!/bin/sh

#
# This script is useful to setup a new development environment, install required
# packages and dependencies, clone the Git repository, set up the database and so on
# to finally run the RunPlayers app.
#

echo "Initial system update"
sudo apt-get update
sudo apt-get upgrade -y

echo "Installing Python development tools..."
sudo apt-get install -y git python python-dev python-virtualenv libpq-dev postgresql libmysqlclient-dev libmemcached-dev zlib1g-dev libssl-dev build-essential libevent-dev python-pip python-dev fabric


# Tenes que crear un USUARIO postgres y contrasenia 1 y database futbolitodomingero_prod
echo "Database setup..."
WHOAMI=$(whoami)
sudo -u postgres psql -c "CREATE ROLE $WHOAMI"
echo "Enter '1' as postgres password when prompted"
echo "\password" | sudo -u postgres psql
#sudo -u postgres psql -c "CREATE DATABASE test_bigcompany"

virtualenv --distribute env
source dev/enter.sh
pip install -U -r requirements.txt
source dev/reset.sh


echo "Installing Heroku Toolbelt"
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh


echo "Running futbolito-domingero in localhost..."
m runserver &
firefox -url "http://localhost:8000/" &

echo "Finish: SUCCESS"

