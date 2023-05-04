#! /usr/bin/bash
set -e

wait_for_ip() {
    echo "Waiting $TIMEOUT seconds for IP..." &>> $LOG
    count=0
    while [ -z $IP ]; do 
        if [ $count -gt $TIMEOUT ]; then
            echo "Timed out waiting for IP. Exiting." &>> $LOG
            exit 0
        fi
        sleep 1
        IP=$(hostname -I | awk '{print $1}')
        count=$((count+1))
    done
    echo "Got IP after $count seconds." &>> $LOG
}

HOSTNAME=$(hostname)
IP=$(hostname -I | awk '{print $1}')
LOG_PATH="~/mbot-logs"
LOG="$LOG_PATH/mbot_publish_info.log"
CONFIG_FILE="/boot/firmware/mbot_config.txt"
GIT_USER=$(grep "^mbot_ip_list_user=" $CONFIG_FILE | cut -d'=' -f2)
GIT_TOKEN=$(grep "^mbot_ip_list_token=" $CONFIG_FILE | cut -d'=' -f2)
GIT_URL=$(grep "^mbot_ip_list_url=" $CONFIG_FILE | cut -d'=' -f2)
GIT_ADDR= ${GIT_URL#*://}
GIT_PATH="~/mbot-ip"
TIMEOUT=30

date > $LOG
echo "Updating IP" &>> $LOG
echo "Hostname= $HOSTNAME" &>> $LOG
if [ -z $IP ]; then 
    wait_for_ip
fi
echo "IP= $IP" &>> $LOG


git -C $GIT_PATH config --local user.email ""
git -C $GIT_PATH config --local user.name "pi"
#git config pull.rebase false
git -C $GIT_PATH pull https://$GIT_USER:$GIT_TOKEN@$GIT_ADDR &>> $LOG

echo "Calling python script" &>> $LOG
python3 $GIT_PATH/main.py -hostname $HOSTNAME -ip $IP -log $LOG
echo "Adding..." &>> $LOG
git -C $GIT_PATH/ add data/$HOSTNAME.json &>> $LOG
echo "Committing..." &>> $LOG
git -C $GIT_PATH/ commit -m "Auto update $HOSTNAME IP" &>> $LOG
echo "Pushing..." &>> $LOG
git -C $GIT_PATH/ push https://$GIT_USER:$GIT_TOKEN@$GIT_ADDR &>> $LOG
echo "Done!" &>> $LOG
exit 0
