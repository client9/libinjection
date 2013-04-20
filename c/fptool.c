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

#include "sqlparse_private.h"
#include "sqli_fingerprints.h"


int main(int argc, const char* argv[])
{
    int ok;

    int offset = 1;

    sfilter sf;
    if (argc < 2) {
        return 1;
    }

    size_t slen = strlen(argv[offset]);

    sfilter_reset(&sf, argv[offset], slen);

    if (slen == 0) {
        return 1;
    }

    /*
     * "plain" context.. test string "as-is"
     */
    ok = is_string_sqli(&sf, argv[offset], slen, CHAR_NULL, is_sqli_pattern);
    if (strlen(sf.pat) > 1) {
        fprintf(stdout, "plain\t%s\t%s\n", sf.pat, ok ? "true": "false");
    }
    if (memchr(argv[offset], CHAR_SINGLE, slen)) {
        ok = is_string_sqli(&sf, argv[offset], slen, CHAR_SINGLE, is_sqli_pattern);
        if (strlen(sf.pat) > 1 && strcmp(sf.pat, "sns") != 0) {
            fprintf(stdout, "single\t%s\t%s\n", sf.pat, ok ? "true": "false");
        }
    }

    if (memchr(argv[offset], CHAR_DOUBLE, slen)) {
        ok = is_string_sqli(&sf, argv[offset], slen, CHAR_DOUBLE, is_sqli_pattern);
        if (strlen(sf.pat) > 1 &&  strcmp(sf.pat, "sns") != 0) {
            fprintf(stdout, "double\t%s\t%s\n", sf.pat, ok ? "true": "false");
        }
    }
    return 0;
}
