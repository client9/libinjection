#!/bin/bash
./autogen.sh
./configure-gprof.sh
make
cd src 
make reader
./libtool --mode=execute ./reader -s -q ../data/sqli-*.txt ../data/false-*.txt
./libtool --mode=execute gprof ./reader gmon.out
