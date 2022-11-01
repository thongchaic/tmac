#!/bin/bash

IP=192.168.6.22

#FILES=('./src/nfd.py' './src/main.py' './src/misc/ping.py' './src/fw/routes.py' './src/config/config.py' './src/fw/fw.py' './src/core/ndn.py' './src/core/sx127x.py' './src/faces/face_table.py' './src/faces/lora.py' './src/faces/mqtt.py' './src/utils/pit.py'  './src/misc/experiments.py')
FILES=('./src/main.py' './src/conf/config.py' './src/core/sx127x.py' './src/core/tmac.py'  './src/inf/lora.py')

kill_proc(){
    exit
}

trap kill_proc SIGINT

for f in "${FILES[@]}"
do

 echo uploading ${f##*/} .......
 /usr/bin/python3 ./webrepl/webrepl_cli.py $f $IP:/${f##*/} -p good2cu
 #./webrepl/webrepl_cli.py $IP:${f##*/} ${f##*/} -p good2cu
 echo -e "\033[0;32m success... \033[0m"
done

# ./webrepl/webrepl_cli.py ./src/misc/wifi.py $IP:main.py -p good2cu
