#!/bin/bash
i=1
while [ $i -le 100000000 ]
do
    id_node=$((1 + $RANDOM % 10))
    timestamp=TZ=UTC date -R
    temperature=$((20 + $RANDOM % 40))
    humidity=$((10 + $RANDOM % 90))
    co2=$((1400 + $RANDOM % 600))
    mysql -uroot -pmypass123 -e "insert into iot.data (id_node,timestamp,temperature,humidity,co2) values ($id_node,$timestamp,$temperature,$humidity,$co2);"
    i=$(($i+1))
    sleep 6 
done
