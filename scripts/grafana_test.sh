sudo mysql -u root
CREATE TABLE sensors;
CREATE TABLE sensors.data ( id INT NOT NULL , timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , value FLOAT NOT NULL );

#!/bin/bash
i=1
while [ $i -le 100000000 ]
do
    id = $((1 + $RANDOM % 10))
    value = $($RANDOM)
    mysql -uroot -pPASSWORD test -e "insert into sensors.data (id,value) values ($id,$value);"
    i=$(($i+1))
    sleep 6 
done