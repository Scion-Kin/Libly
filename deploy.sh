#!/usr/bin/bash
## ./deploy.sh
## Deploys a web app to given servers
## Copyright (C) 2025 Buffer Park

# Bold colors
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
Color_Off='\033[0;37m'    # White

# TODO: Add host discovery so that users can use domain names instead of IP addresses

# Exit if any command returns a non-zero status (command failed). This also ensures that I get the error output of the command that failed. 
set -e

# Check if three arguments are provided
if [ $# -lt 1 ]; then
    echo -e "${BRed}Usage: ./deploy.sh server_name1 ...servicelist ${Color_Off}"
    exit 1
fi

cd ..

# Store arguments in variables
servers=("$1")
inputFile=Libly
dtime="$(date +'%Y%m%d%H%M%S')"
file="$inputFile$dtime"

if [ ! -d "$inputFile" ]; then
    echo -e "${BRed}Error: Input directory '$inputFile' does not exist.${Color_Off}"
    exit 1
fi

if [ $3 ]; then
    shift 3
    services=("$@")
else
    services=("nginx")
fi

deploy_dir="${DEPLOY_DIR:-~/.Libly/releases}"

# Prompt and countdown
echo -e "${BYellow}Please note does not provide graceful error handling, so that you don't live with a broken app.${Color_Off}\n"
echo ""
echo -e "${BCyan}After this operation, the deployed version will be stored in the folder 'versions/'"
echo ""
echo "Deployment will commence in 10 seconds. Check if you entered correct information."
echo ""
echo -e "Press ctrl c, to cancel if you made a mistake.${Color_Off}"
echo ""

for ((j=10; j>0; j--)); do
    echo -ne "${BYellow}Starting deployment in $j seconds...\r${Color_Off}"
    sleep 1
done

# Display archive name and deployment servers
echo -e "\n${BCyan}Your new archive will be named:${Color_Off}\t$file\n"

echo -e "${BCyan}Deploying to the following servers:${Color_Off}"
echo ""
for i in "${servers[@]}"; do
    printf "\t%s\n" "$i" 
done

# Create versions directory if it doesn't exist
if [ ! -d "$inputFile/versions" ]; then
    mkdir "$inputFile/versions/"
fi

# Create and transfer archive, then deploy to servers
tar -czf "$inputFile/versions/$file.tgz" "$inputFile"

for i in "${servers[@]}"; do
	(
    echo ""
    echo -e "${BBlue}Deploying on server: ${BYellow}\t$i\t...\n${Color_Off}"
    scp -i ~/.ssh/id_rsa "$inputFile/versions/$file.tgz" "ubuntu@$i:/tmp/"
    echo ""
    echo -e "${BGreen}Copied archive file to server:${Color_Off}\t$i in directory:\t/tmp/"
    echo ""
    echo -e "${BBlue}Extracting archive to:${Color_Off}\t$deploy_dir/ ..."
    echo ""
    ssh ubuntu@"$i" "mkdir -p $deploy_dir/new && tar -xzf /tmp/$file.tgz -C $deploy_dir/new && mv $deploy_dir/new/$inputFile $deploy_dir/$file"
    echo -e "${BCyan}Here are the new contents of the releases directory:${Color_Off}"
    echo ""
    ssh ubuntu@"$i" "sudo rm -rf $deploy_dir/new/ && ls $deploy_dir/ | sed 's/^/\t\t\t/' && sudo rm -rf ~/.Libly/current && ln -s $deploy_dir/$file ~/.Libly/current"
    echo -e "\n${BGreen}Finished making a symbolic link for the new web static${Color_Off}"
    echo ""
    # Before restartig nginx, check if it's installed on the server (restart other services also)
    ssh ubuntu@"$i" "sudo rm -rf /tmp/$file.tgz && \
        if dpkg -l | grep -q '^ii  nginx'; then \
            echo '✅ Nginx is installed, restarting Nginx server...'; \
            sudo systemctl restart nginx ${services[@]} && \
            echo '✅ Services restarted successfully.'; \
        else \
            echo '❌ Nginx is not installed, skipping restart.'; \
            sudo systemctl restart ${services[@]} && \
            echo '✅ Services restarted successfully.'; \
        fi"
    echo ""
    echo -e "${BGreen}Deleted the archive from /tmp/, and restarted the Nginx server and all services.${Color_Off}"
    echo ""
    echo -e "${BGreen}Your newest app release ($file) is now live on -> ($i)!${Color_Off}"
    echo -e "You can visit: $i/ to use app if the services are set up correctly."
	) &
done

wait

# Final message
echo -e "${BGreen}Deployment complete"
