#!/bin/bash

rm -f testdriver

scan-build --status-bugs -no-failure-reports \
-enable-checker alpha.core.BoolAssignment \
-enable-checker alpha.core.CastSize \
-enable-checker alpha.core.CastToStruct \
-enable-checker alpha.core.FixedAddr \
-enable-checker alpha.core.PointerArithm \
-enable-checker alpha.core.PointerSub \
-enable-checker alpha.core.SizeofPtr \
-enable-checker alpha.deadcode.IdempotentOperations \
-enable-checker alpha.deadcode.UnreachableCode \
-enable-checker alpha.security.ArrayBound \
-enable-checker alpha.security.ArrayBoundV2 \
-enable-checker alpha.security.MallocOverflow \
-enable-checker alpha.security.ReturnPtrRange \
-enable-checker alpha.unix.cstring.BufferOverlap \
-enable-checker alpha.unix.cstring.OutOfBounds \
-enable-checker security.FloatLoopCounter \
-enable-checker security.insecureAPI.rand \
-enable-checker security.insecureAPI.strcpy \
make testdriver
