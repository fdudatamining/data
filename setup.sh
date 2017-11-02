#!/bin/sh

MYSQL_HOST="$1"
MYSQL_ROOT_PASSWORD="$2"

cd /root/

if [ ! -f setup ]; then
  echo "Waiting for database to respond..."
  while ! mysqladmin ping --host=$MYSQL_HOST --silent; do
    sleep 1;
  done
  echo "Initializing database..."
  MYSQL_HOST=$MYSQL_HOST MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD python3 ./setup.py install
  touch setup
fi
