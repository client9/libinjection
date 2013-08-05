#!/usr/bin/env python

if __name__ == '__main__':
    if len(sys.argv) == 2:
        fh = open(sys.argv[1], 'r')
    else:
        fh = sys.stdin

    for line in fh:
        line = line.replace("\\x", "%").strip()
        try:
            data = json.loads(line)
        except ValueError, e:
            data = None

        if data is None:
            continue

        if int(data['status']) != 200 or data['ssl_protocol'] == '':
            continue

        print "\t".join( (data['ssl_protocol'], data['ssl_cipher'], data['http_user_agent']))
