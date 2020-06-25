#!/bin/bash

# create conky configurations
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_devconn      ./DATA/left_devconn 
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_netdev       ./DATA/left_netdev 
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_netapscan    ./DATA/left_netapscan 
./bin/make_left.py ./DATA/LEFT/config ./DATA/LEFT/left_inconn       ./DATA/left_inconn 

./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_summary    ./DATA/right_summary
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_battery    ./DATA/right_battery 
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_memory     ./DATA/right_memory
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_cpu        ./DATA/right_cpu 
./bin/make_left.py ./DATA/LEFT/config ./DATA/RIGHT/right_hd         ./DATA/right_hd

# startup several conky instances, 1 for each configuration
sleep 2 && conky -dc ./DATA/left_devconn   
sleep 2 && conky -dc ./DATA/left_netdev    
sleep 2 && conky -dc ./DATA/left_netapscan 
sleep 2 && conky -dc ./DATA/left_inconn    
sleep 2 && conky -dc ./DATA/right_summary  
sleep 2 && conky -dc ./DATA/right_battery  
sleep 2 && conky -dc ./DATA/right_memory   
sleep 2 && conky -dc ./DATA/right_cpu      
sleep 2 && conky -dc ./DATA/right_hd      

