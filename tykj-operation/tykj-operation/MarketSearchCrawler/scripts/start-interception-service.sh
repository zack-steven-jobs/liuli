#!/bin/bash - 
#===============================================================================
#
#          FILE: start-interception-service.sh
# 
#         USAGE: ./start-interception-service.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2013年09月13日 10时46分50秒 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error


oldpwd=`pwd`
this_file=$0
if [[ -h $0 ]];then
    this_file=`ls -l $0|awk -F"->" '{print $2}'`
fi
ws=`dirname $this_file`
cd $ws
ws=`pwd`

mkdir -p /var/app/log/MarketSearchCrawler 
chmod a+rw /var/app/log/MarketSearchCrawler

export PYTHONPATH=/var/app/enabled/MarketSearchCrawler
cd ..
python services/interception/rabbitmq_consumer.py >> /var/app/log/MarketSearchCrawler/interception_service.log 2>&1

cd $oldpwd
exit 0


