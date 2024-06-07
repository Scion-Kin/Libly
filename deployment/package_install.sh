#!/usr/bin/env bash

sudo apt-get install gunicorn
sudo apt-get install python3
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install certbot
sudo apt-get install mysql-client
sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential
pip3 install -r requirements.txt
sudo npm install -g nodemailer express body-parser cors
