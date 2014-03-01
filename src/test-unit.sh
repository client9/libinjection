#!/bin/bash
set -e
cd ../tests
pwd

find . -name 'test*.txt' | xargs ../src/testdriver
