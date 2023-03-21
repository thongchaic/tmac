#!/bin/bash

IP=10.3.0.x

FILES=('./src/main.py' './src/fw/fw.py' './src/fw/tokens.py' './src/fw/names.py' './src/core/simple.py' './src/conf/config.py' './src/core/sx127x.py' './src/core/tmac.py'  './src/inf/lora.py'  './src/inf/mqtt.py')

kill_proc(){
    exit
}

trap kill_proc SIGINT

for f in "${FILES[@]}"
do

 echo uploading ${f##*/} .......
 /usr/bin/python3 ./webrepl/webrepl_cli.py $f $IP:/${f##*/} -p good2cu
 echo -e "\033[0;32m success... \033[0m"
done

#./webrepl/webrepl_cli.py ./src/gateway.py $IP:main.py -p good2cu
#./webrepl/webrepl_cli.py ./src/mote.py $IP:main.py -p good2cu
