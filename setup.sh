#!/bin/sh

MYSQL_HOST="$1"
MYSQL_ROOT_PASSWORD="$2"

cd /root/

echo "Waiting for database to respond..."
while ! mysqladmin ping --host=$MYSQL_HOST --silent; do
  sleep 1;
done

echo "Creating database..."
( cat | mysql --host=$MYSQL_HOST --user=root --password=$MYSQL_ROOT_PASSWORD ) << END
create database datamining;
use datamining;
END

echo "Building tables..."
MYSQL_HOST=$MYSQL_HOST MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD python3 ./setup.py install

