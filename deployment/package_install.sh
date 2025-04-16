#!/usr/bin/env bash

## ./package_install.sh
## Installs all the packages required for the Libly project

WD=$(pwd)
# Check if the script is run in the correct directory
if [[ $WD != *"Libly"* ]]; then
    printf "\033[1;31m This script must be run in the Libly directory. Please run it in the Libly directory.\n"
    exit 1
fi

# go back to the parent directory if we're in the deployment subdirectory
if [[ $WD == *"deployment"* ]]; then
    cd ..
    WD=$(pwd)
fi
echo "$WD"

set -e

sudo apt update && sudo apt upgrade -y
if ! command -v zsh &> /dev/null
then
    read -p "\033[1;35mZsh is not installed. It is our favorite shell, and our deployment depends on it. Do you want to install it? (y/n) " answer
    if [[ $answer == "y" ]]; then
        sudo apt install zsh git -y
    else
        echo "zsh is required to run this script. Exiting..."
        exit 1
    fi
fi
# Install oh-my-zsh
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

sudo apt-get install nginx -y
sudo apt-get install gunicorn -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
curl -sL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install certbot python3-certbot-nginx -y
sudo apt-get install mysql-client mysql-server -y
sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential -y
sudo apt install python3-venv -y

## The venv should be outside of current version, to prevent having to reinstall dependencies on every release
cd .. && python3 -m venv venv
source venv/bin/activate
pip3 install --quiet --upgrade pip
pip3 install -r "$WD/deployment/requirements.txt"
cd -
cd node_api
npm install ## Reintalling these dependencies can't be avoided for now.
cd ..

printf "\033[1;32mAll packages installed successfully. \n\n"
printf "\033[1;33mPlease run the server_setup.sh script to set up the server. \n\n"
