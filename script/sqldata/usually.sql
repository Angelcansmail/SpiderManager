-- 导出数据库
mysqldump -uroot -p datap> Dump20181009.sql
-- 关联ip和port表
select a.ip,port,hostname,name,product,version,hackinfo,timesearch from snifferdata a join ip_maindata b on (a.ip=b.ip and hackinfo like'%hole%');
