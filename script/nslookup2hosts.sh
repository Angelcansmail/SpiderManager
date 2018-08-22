#!/bin/sh
echo "the hosts are:"
nslookup $1 8.8.8.8 |grep Add |awk -F " " '{printf $2 "   nenew.net\n"}' |sed /#/d|sed s/nenew.net/$1/g
