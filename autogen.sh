#!/bin/sh

# autoconf 2.68 requires the m4 directory to
#  exist.  2.69 makes it for you.
if [ ! -d m4 ]; then mkdir m4; fi

autoreconf --install
automake --add-missing >/dev/null 2>&1
