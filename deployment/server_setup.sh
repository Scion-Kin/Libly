#!/usr/bin/env bash

set -e

sudo apt install gunicorn -y
sudo apt install nginx -y

nginx_conf=\
"
# Default server configuration

server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name usernet.tech web-01.usernet.tech; # change the domain if any domain changes have occured

        # Redirect all HTTP requests to HTTPS
        #return 301 https://$host$request_uri;

        add_header X-Served-By 322536-web-01;

        client_max_body_size 100M;

        location /api/ {
                include proxy_params;
                proxy_pass http://0.0.0.0:5000/api/;
        }

        location / {
                include proxy_params;
                proxy_pass http://0.0.0.0:5050/;
        }

        location /static {
                include proxy_params;
                proxy_pass http://0.0.0.0:5050/;
        }

        location /mail {
                include proxy_params;
                proxy_pass http://0.0.0.0:3000/;
        }
}
"

flask_api_service=\
"
[Unit]
Description=Gunicorn instance to serve the flask APi
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
'
[Unit]
Description=Node instance to serve the node API
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Libly/node_api/
Environment="NODE_PATH=/usr/lib/node_modules"
ExecStart=/usr/bin/node /home/ubuntu/Libly/node_api/app.js

[Install]
WantedBy=multi-user.target
'

web_server_service=\
"
[Unit]
Description=Gunicorn instance to serve the web server
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Libly/
ExecStart=gunicorn --workers 4 --bind 0.0.0.0:5050 --access-logfile /tmp/web_server.log --error-logfile /tmp/web_server-error.log web_client.app:app

[Install]
WantedBy=multi-user.target
"

echo "$nginx_conf" | sudo tee /etc/nginx/sites-available/default > /dev/null
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
echo "$flask_api_service" | sudo tee /etc/systemd/system/flask_api.service > /dev/null
echo "$node_api_service" | sudo tee /etc/systemd/system/node_api.service > /dev/null
echo "$web_server_service" | sudo tee /etc/systemd/system/web_server.service > /dev/null
cat setup_mysql_dev.sql | sudo mysql -u root
sudo service start mysql
sudo systemctl daemon-reload
sudo systemctl enable mysql
sudo systemctl enable flask_api
sudo systemctl enable node_api
sudo systemctl enable web_server
sudo service flask_api start
sudo service node_api start
sudo service web_server start
sudo service nginx start
