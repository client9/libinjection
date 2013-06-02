#!/usr/bin/env python

def make_lua_table(obj):
    fp = obj[u'fingerprints']
    print("sqlifingerprints = {")
    for f in fp:
        print('  ["{0}"]=true,'.format(f))
    print("}")
    return 0

if __name__ == '__main__':
    import sys
    import json
    sys.exit(make_lua_table(json.load(sys.stdin)))
