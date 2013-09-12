#!/bin/bash
git status | grep -v '#'

NUMBER=`grep LIBINJECTION_VERSION c/libinjection.h | head -1 | awk '{print $3}' | tr -d '"'`
VERSION="v${NUMBER}"
echo git tag -a $VERSION -m ${VERSION}
git tag -a $VERSION -m ${VERSION}
echo git push origin $VERSION
git push origin $VERSION



