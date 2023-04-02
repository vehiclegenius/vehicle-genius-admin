#!/usr/bin/env bash

# Exit on first error
set -e

sudo supervisorctl stop vehicle-genius-admin

./build.sh

sudo supervisorctl reread vehicle-genius-admin
sudo supervisorctl update vehicle-genius-admin
sudo supervisorctl restart vehicle-genius-admin
