#!/system/bin/sh

#================================================================
#   Copyright (C) 2018 Sangfor Ltd. All rights reserved.
#   
#   文件名称：sniffertool.sh
#   创 建 者：Gangzh
#   创建日期：2018年08月10日
#   描    述：
#
#================================================================

nohup python sniffertool.py > logs/sniffertool.log 2>logs/sniffertool.err &
