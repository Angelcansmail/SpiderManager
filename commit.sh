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

rm `find -name "*.err"`
rm `find -name "*.log"`
rm `find -name "*.pyc"`
mv SpiderManager/settings.py elasticsearchmanage/elastictool.py elasticsearchmanage/mapping.py spidertool/config.py ../
git add *
git commit -m "$content"
git push origin master

mv ../elastictool.py ../mapping.py elasticsearchmanage/
mv ../settings.py SpiderManager/
mv ../config.py spidertool/
# 获取大文件列表
# git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -5 | awk '{print$1}')"

# 删除git上的大文件
# git filter-branch -f --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch xxxxx' --tag-name-filter cat -- --all
