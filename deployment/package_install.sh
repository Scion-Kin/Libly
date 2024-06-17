#!/usr/bin/env bash

sudo apt-get install nginx -y
sudo apt-get install gunicorn -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install certbot python3-certbot-nginx -y
sudo apt-get install mysql-client mysql-server -y
sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential -y
pip3 install -r requirements.txt
sudo npm install -g nodemailer express body-parser cors
