#!/bin/bash  

rm ${1}_ip
while read host
do
    echo $host"\t" `nslookup -sil $host 2>/dev/null | grep Address: | sed '1d' | sed 's/Address: //g'` >> ${1}_ip
#    echo $host"\t" `nslookup $host | grep "Address: " | cut -d" " -f 2 ` >> ${1}_ip
#    echo $host"\t" `nslookup $host | grep "Address: " | sed -i "s/Address: //g" ` >> ${1}_ip
done < $1

cat ${1}_ip
cat ${1}_ip | awk -F'\t ' '{if(length($2) > 0) print $2}' | tr ' ' '\n' | awk '{print $0"/24"}'> ${1}_iparea.json
