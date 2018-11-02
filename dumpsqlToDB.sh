cur_date="`date +%Y-%m-%d`"
####init database mysqldump -uroot -p datap > Dump${cur_date}.sql
echo $(cur_date)
init_sql="source $(pwd)/script/sqldata/Dump20181009.sql"
result=$(mysql -uroot -p${passwd} -Ddatap -s -e "${init_sql}")
