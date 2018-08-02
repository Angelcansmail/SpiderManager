#!/system/bin/sh

#================================================================
#   Copyright (C) 2018 Sangfor Ltd. All rights reserved.
#   
#   文件名称：commit.sh
#   创 建 者：Gangzh
#   创建日期：2018年07月30日
#   描    述：
#
#================================================================

content=$1

rm *.pyc
rm */*.pyc
rm */*/*.pyc
rm */*/*/*.pyc
git add *
git commit -m "$content"
git push origin master
