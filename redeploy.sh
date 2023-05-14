#!/usr/bin/env bash

# Exit on first error
set -e

sudo supervisorctl stop vehicle_genius_admin

for pid in $(ps aux | grep 'manage.py' | awk '{print $2}'); do
  # we ignore any errors during killing
  sudo kill $pid || :
done

./build.sh

sudo supervisorctl reread
sudo supervisorctl update vehicle_genius_admin
sudo supervisorctl restart vehicle_genius_admin
