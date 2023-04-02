# Setup instructions for server

Assumptions:

- Running on a DigitalOcean Ubuntu droplet
- Using supervisorctl for managing the process
- All is running on `dimo` user

## Dependencies

- Python 3+

## Nginx

```shell
sudo apt-get update
sudo apt-get install nginx
sudo cp nginx.conf /etc/nginx/sites-available/vehicle-genius-admin
sudo ln -s /etc/nginx/sites-available/vehicle-genius-admin /etc/nginx/sites-enabled
```

## Gunicorn

```shell
pip install gunicorn
```

## supervisorctl

```shell
sudo apt-get update
sudo apt-get install supervisor
cp supervisorctl.conf /etc/supervisor/conf.d/vehicle-genius-admin.conf
```

## Configuration

```shell
cp .env.example .env
```

Configure as appropriate.
