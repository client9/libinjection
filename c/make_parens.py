#!/usr/bin/env python

import sys

def main():
    """
     this "doubles all parathensis"
     to make new fingerprints
     """

    for line in sys.stdin:
        fp = line.strip()
        print fp

        if '(' in fp:

            done = False
            parts = []
            for c in fp:
                if c == '(' and done is False:
                    parts.append(c)
                    done = True
                parts.append(c)
            newline = ''.join(parts)[0:5]
            print newline

            done = False
            parts = []
            for c in fp:
                if c == '(':
                    if done is True:
                        parts.append(c)
                    else:
                        done = True
                parts.append(c)
            newline = ''.join(parts)[0:5]
            print newline

            done = False
            parts = []
            for c in fp:
                if c == '(':
                    parts.append(c)
                parts.append(c)
            newline = ''.join(parts)[0:5]
            print newline


if __name__ == '__main__':
    main()


