#!/usr/bin/env bash

# Exit on first error
set -e

sudo supervisorctl stop vehicle_genius_admin || true

./build.sh

sudo supervisorctl reread
sudo supervisorctl update vehicle_genius_admin
sudo supervisorctl restart vehicle_genius_admin
