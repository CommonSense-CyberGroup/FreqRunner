#!/usr/bin/bash

## NOTE -- This is the laegacy way to use OP25! We are now moving to using the multi_rx.py script that used the cfg.json file to gather all of the configuration!

#This is the kick-off line that will  start both OP25 using our trunk file, as well as starting up the HTTP interface for the user
#This has all of the options as well as the trunk file name that is used in the actual freqWalker script
./rx.py --nocrypt --args "rtl" --gains 'lna:36' -S 960000 -X -q 0 -l 'http:0.0.0.0:8082' -v 1 -2 -V -U -T freq_walker_trunk.tsv 2> stderr.2
