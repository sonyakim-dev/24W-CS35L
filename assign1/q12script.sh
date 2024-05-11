#!/bin/bash

curr=$$
list=$$

# Get ancestors
# iterate to get a list of ppid separated by ","
while [ "$curr" -ne 1 ]
do
    curr=$(ps -o ppid= -p $curr)
    list=$curr,$list
done

list=$(echo $list | tr -d ' \n') # remove space and newline

ps -f --forest -p $list --ppid $$
