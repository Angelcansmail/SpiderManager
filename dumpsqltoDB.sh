####init database
echo $(pwd)
init_sql="source $(pwd)/script/sqldata/Dump20181009.sql"
result=$(mysql -uroot -pgzh123 -Ddatap -s -e "${init_sql}")
