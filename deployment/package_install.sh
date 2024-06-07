#!/usr/bin/env bash

sudo apt-get install gunicorn -y
sudo apt-get install python3 -y
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install certbot -y
sudo apt install certbot python3-certbot-nginx -y

echo "..." && echo "Hi there, the certbot script which is going to set up your https is going to start"
echo "..." && echo "Please follow the prompts carefully" && echo "..."

sudo certbot --nginx
sudo apt-get install mysql-client mysql-server -y
sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential -y
pip3 install -r requirements.txt
sudo npm install -g nodemailer express body-parser cors
