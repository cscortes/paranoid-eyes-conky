#!/bin/bash

# --------------------------------------------------
#
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_devconn      ./DATA/left_devconn 
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_netdev       ./DATA/left_netdev 
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_netapscan    ./DATA/left_netapscan 
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_inconn       ./DATA/left_inconn 

conky -c ./DATA/left_devconn &
conky -c ./DATA/left_netdev &
conky -c ./DATA/left_netapscan &
conky -c ./DATA/left_inconn &

./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_summary ./DATA/right_summary
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_battery ./DATA/right_battery 
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_memory  ./DATA/right_memory
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_cpu     ./DATA/right_cpu 
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_hd      ./DATA/right_hd

sleep 5
conky -c ./DATA/right_summary &
sleep 5
conky -c ./DATA/right_battery &
sleep 5
conky -c ./DATA/right_memory &
sleep 5
conky -c ./DATA/right_cpu &
sleep 5
conky -c ./DATA/right_hd &
