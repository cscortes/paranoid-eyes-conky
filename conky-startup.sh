#!/bin/bash
# conky -c ~/.conky/right_conkyrc &
sleep 4
conky -c ~/.conky/DATA/right_summary &
conky -c ~/.conky/DATA/left_devconn &
sleep 2
conky -c ~/.conky/DATA/right_battery &
conky -c ~/.conky/DATA/left_netdev &
sleep 2
conky -c ~/.conky/DATA/right_memory &
conky -c ~/.conky/DATA/left_netapscan &
sleep 2
conky -c ~/.conky/DATA/right_cpu &
sleep 2
conky -c ~/.conky/DATA/right_hd &
conky -c ~/.conky/DATA/left_inconn &
