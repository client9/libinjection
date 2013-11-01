#!/bin/bash

rm -f testdriver

scan-build --status-bugs \
-enable-checker alpha.core.BoolAssignment \
-enable-checker alpha.core.CastSize \
-enable-checker alpha.core.CastToStruct \
-enable-checker alpha.core.FixedAddr \
-enable-checker alpha.core.PointerArithm \
-enable-checker alpha.core.SizeofPtr \
-enable-checker alpha.deadcode.IdempotentOperations \
-enable-checker alpha.deadcode.UnreachableCode \
-enable-checker alpha.security.ArrayBound \
-enable-checker alpha.security.MallocOverflow \
-enable-checker alpha.security.ReturnPtrRange \
-enable-checker alpha.unix.cstring.BufferOverlap \
-enable-checker alpha.unix.cstring.OutOfBounds \
-enable-checker security.FloatLoopCounter \
-enable-checker security.insecureAPI.rand \
make testdriver

# notes 2013-10-24

# do not understand
# -no-failure-reports

# seems broken or I don't understand it
# -enable-checker alpha.core.PointerSub

#
# probably good.. used in testdriver as a hack
#-enable-checker security.insecureAPI.strcpy

# has problem with "backwards array iteration"
# used in is_backslash_escaped
#-enable-checker alpha.security.ArrayBoundV2
