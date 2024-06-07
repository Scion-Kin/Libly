#!/usr/bin/env bash

sudo apt install gunicorn
sudo apt install python3
sudo apt install nodejs # replace with the actual latest install procedure
sudo apt install certbot
pip3 install -r requirements.txt
npm install -g nodemailer express body-parser cors
