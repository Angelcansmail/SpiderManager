#!/bin/sh
bin=${JDBC_IMPORTER_HOME}/bin
lib=${JDBC_IMPORTER_HOME}/lib

java \
    -cp "${lib}/*" \
    -Dlog4j.configurationFile=${bin}/log4j2.xml \
    org.xbib.tools.Runner \
    org.xbib.tools.JDBCImporter $1
