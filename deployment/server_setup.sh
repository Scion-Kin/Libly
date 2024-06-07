#!/usr/bin/env bash

set -e

sudo apt install gunicorn -y
sudo apt install nginx -y

nginx_conf=\
"
# Default server configuration
server {
        listen 80;
        server_name usernet.tech web-01.usernet.tech; # change the domain if any domain changes have occured

        # Redirect all HTTP requests to HTTPS
        return 301 https://$host$request_uri;
}

server {
        listen 443 ssl;

        add_header X-Served-By 322536-web-01;

        server_name usernet.tech web-01.usernet.tech; # change the domain if any domain changes have occured

        location /api/ {
                include proxy_params;
                proxy_pass http://0.0.0.0:5000/api/;
        }

        client_max_body_size 100M;

        location / {
                include proxy_params;
                proxy_pass http://0.0.0.0:5050/;
        }

        location /static {
                include proxy_params;
                proxy_pass http://0.0.0.0:5050/;
        }
}
"

flask_api_service=\
"
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Libly/
ExecStart=gunicorn --workers 4 --bind 0.0.0.0:5000 --access-logfile /tmp/flask_api.log --error-logfile /tmp/flask_api-error.log flask_api.v1.app:app

[Install]
WantedBy=multi-user.target
"

node_api_service=\
"
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Libly/node_api/
PATH=/usr/lib/node_modules
ExecStart=node app.js

[Install]
WantedBy=multi-user.target
"

web_server_service=\
"
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Libly/
ExecStart=gunicorn --workers 4 --bind 0.0.0.0:5050 --access-logfile /tmp/web_server.log --error-logfile /tmp/web_server-error.log web_client.app:app

[Install]
WantedBy=multi-user.target
"

sudo chown -R nginx:$USER /etc/nginx
sudo echo "$nginx_conf" > /etc/nginx/sites-available/default
sudo ln -s /etc/nginx/sites-available /etc/nginx/sites-enabled
sudo echo "$flask_api_service" > /etc/systemd/system/flask_api.service
sudo echo "$node_api_service" > /etc/systemd/system/node_api.service
sudo echo "$web_server_service" > /etc/systemd/system/web_server.service
sudo service flask_api start
sudo service node_api start
sudo service web_server start
sudo service nginx start
