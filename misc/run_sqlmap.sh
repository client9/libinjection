#!/bin/bash

# Starts a bogus webserver that logs all input
# Then runs sqlmap
#

./nullserver.py &

if [ -d "sqlmap-dev" ]; then
    svn checkout https://svn.sqlmap.org/sqlmap/trunk/sqlmap sqlmap-dev
else
    (cd sqlmap-dev; svn up)
fi

SQLMAP=./sqlmap-dev/sqlmap.py
URL=http://127.0.0.1:8888
${SQLMAP} -v 0 -p id --level=5 --risk=3 --url=${URL}/null?id=1
${SQLMAP} -v 0 -p id --level=5 --risk=3 --url=${URL}/null?id=1234.5
${SQLMAP} -v 0 -p id --level=5 --risk=3 --url=${URL}/null?id=foo

curl -o /dev/null ${URL}/shutdown

