#!/bin/bash
# conky -c ~/.conky/right_conkyrc &
sleep 4
conky -c ~/.conky/DATA/right_summary &
sleep 1
conky -c ~/.conky/DATA/right_battery &
sleep 1
conky -c ~/.conky/DATA/right_memory &
sleep 1
conky -c ~/.conky/DATA/right_cpu &
sleep 1
conky -c ~/.conky/DATA/right_hd &
sleep 6
conky -c ~/.conky/DATA/left_conkyrc &
