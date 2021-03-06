#!/bin/bash - 
#===============================================================================
#
#          FILE: clean.sh
# 
#         USAGE: ./clean.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 12/06/2013 03:01:05 PM CST
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

data_dir=/var/app/data/MarketSearchCrawler/clean_apk/
sudo mkdir -p $data_dir && sudo chmod a+rw $data_dir
cd $data_dir

log_file=deleted_files.log
log_level=DEBUG
test -f $log_file && (cat $log_file >> $log_file.bak && cat /dev/null > $log_file)
source $ws/logger.sh

top_count=100000
start_time=`date '+%Y-%m-%d %H:%M:%S'`
end_time=
mail_to=gmliao@bainainfo.com,jliang@bainainfo.com,jjpan@bainainfo.com,zhxtang@bainainfo.com,jli@bainainfo.com,lyliu@bainainfo.com

function init_data()
{
    local sql="select package_name, sum(cast(downloads as unsigned))/count(id) as d_avg from final_app where file_type='apk' and created_at < date_sub(now(), interval 7 day) group by package_name order by d_avg desc"
    exec_sql "$sql" > package_desc_downloads
    tail -n+2 package_desc_downloads | head -n$top_count | cut -f1 > package_top
    tail -n+$(($top_count + 2)) package_desc_downloads | cut -f1 > package_tail
}

function exec_sql()
{
    mysql -udev_market -pmarket_dev_pwd -h192.168.130.77 market -e "$1"
}

function clean_apk()
{
    local pn=$1
    local limit_start=$2
    log_info clean apk for pn=$pn, limit_start=$limit_start start.
    local sql="select id, version, version_code, concat('/mnt/ctappstore*/vol', vol_id, '/', file_path) from final_app where package_name = \"$pn\" and created_at < date_sub(now(), interval 7 day) order by version_code desc limit $limit_start,100;"
    exec_sql "$sql" | tail -n+2 | while read id version version_code file_path; do
        local apk_info="id=$id, version=$version, version_code=$version_code, file_path=$file_path"
        log_info handle file: $file_path.
        if ls $file_path 1>/dev/null 2>&1; then
            if [[ `ls $file_path | wc -l` -eq 1 ]]; then
                sudo rm $file_path
                log_info delete file: $file_path. $apk_info
            else
                log_error more than one file found for file: $file_path, will not delete. $apk_info
            fi
        else
            log_error file $file_path does not exist. $apk_info
        fi
    done
    log_info clean apk for pn=$pn, limit_start=$limit_start end.
}

function send_statistics_mail()
{
    local handled_app_count=$(cat $log_file | grep "clean apk.*start" | wc -l)
    local handled_file_count=$(cat $log_file | grep "handle file: " | wc -l)
    local deleted_file_count=$(cat $log_file | grep "delete file:" | wc -l)
    local can_not_handle_file_count=$(cat $log_file | grep "more than one file" | wc -l)
    local not_exist_file_count=$(cat $log_file | grep "does not exist." | wc -l)
    test -f mail && (cat mail >> mail.log && cat /dev/null > mail)
    (echo "Clean apk started at: $start_time, ended at: $end_time."; \
    echo ""; \
    echo "Handled app count: $handled_app_count"; \
    echo "Handled file count: $handled_file_count"; \
    echo "Deleted file count: $deleted_file_count"; \
    echo "Could not handle file count: $can_not_handle_file_count"; \
    echo "Not exist file count: $not_exist_file_count" ;) >> mail
    cat mail | mail -s "Clean Apk Task Report -- $start_time" $mail_to
}


function main()
{
    init_data
    cat package_top | while read pn; do clean_apk $pn 4; done
    cat package_tail | while read pn; do clean_apk $pn 1; done
    end_time=`date '+%Y-%m-%d %H:%M:%S'`
    send_statistics_mail
}


log_info "clean apk files start."
main
log_info "clean apk files end."

cd $oldpwd
exit 0
