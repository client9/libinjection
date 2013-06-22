/**
 * Copyright 2012, 2013 Nick Galbreath
 * nickg@client9.com
 * BSD License -- see COPYING.txt for details
 *
 * This is for testing against files in ../data/ *.txt
 * Reads from stdin or a list of files, and emits if a line
 * is a SQLi attack or not, and does basic statistics
 *
 */
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


#include "libinjection.h"

int main(int argc, const char* argv[])
{
    int ok;

    int offset = 1;

    sfilter sf;
    if (argc < 2) {
        return 1;
    }

    size_t slen = strlen(argv[offset]);

    if (slen == 0) {
        return 1;
    }

    /*
     * "plain" context.. test string "as-is"
     */
    libinjection_sqli_init(&sf, argv[offset], slen, 0);

    libinjection_sqli_fingerprint(&sf, FLAG_QUOTE_NONE | FLAG_SQL_ANSI);
    ok = libinjection_sqli_check_fingerprint(&sf);
    fprintf(stdout, "plain-asni\t%s\t%s\n", sf.fingerprint, ok ? "true": "false");

    libinjection_sqli_fingerprint(&sf, FLAG_QUOTE_NONE | FLAG_SQL_MYSQL);
    ok = libinjection_sqli_check_fingerprint(&sf);
    fprintf(stdout, "plain-mysql\t%s\t%s\n", sf.fingerprint, ok ? "true": "false");

    libinjection_sqli_fingerprint(&sf, FLAG_QUOTE_SINGLE | FLAG_SQL_ANSI);
    ok = libinjection_sqli_check_fingerprint(&sf);
    fprintf(stdout, "single-ansi\t%s\t%s\n", sf.fingerprint, ok ? "true": "false");

    libinjection_sqli_fingerprint(&sf, FLAG_QUOTE_SINGLE | FLAG_SQL_MYSQL);
    ok = libinjection_sqli_check_fingerprint(&sf);
    fprintf(stdout, "single-mysql\t%s\t%s\n", sf.fingerprint, ok ? "true": "false");

    libinjection_sqli_fingerprint(&sf, FLAG_QUOTE_DOUBLE | FLAG_SQL_MYSQL);
    ok = libinjection_sqli_check_fingerprint(&sf);
    fprintf(stdout, "double-mysql\t%s\t%s\n", sf.fingerprint, ok ? "true": "false");

    return 0;
}
