FILES=('joinrequest-206.json' 'publish-250-206.json' 'publish-500-206.json' 'publish-750-206.json' 'subscribe-206.json')
IP=192.168.1.x

for f in "${FILES[@]}"
do
 echo download ${f##*/} .......
 /usr/bin/python3 ./webrepl/webrepl_cli.py $IP:/${f##*/} ./results/$f -p good2cu
 #./webrepl/webrepl_cli.py $IP:${f##*/} ${f##*/} -p good2cu
 echo -e "\033[0;32m success... \033[0m"
done