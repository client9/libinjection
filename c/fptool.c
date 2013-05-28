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
    libinjection_sqli_fingerprint(&sf, argv[offset], slen,
                                  CHAR_NULL, COMMENTS_ANSI);
    ok = libinjection_is_sqli_pattern(&sf, NULL);
    fprintf(stdout, "plain-asni\t%s\t%s\n", sf.pat, ok ? "true": "false");

    if (sf.stats_comment_ddx) {
        libinjection_sqli_fingerprint(&sf, argv[offset], slen,
                                      CHAR_NULL, COMMENTS_MYSQL);
        ok = libinjection_is_sqli_pattern(&sf, NULL);
        fprintf(stdout, "plain-mysql\t%s\t%s\n", sf.pat, ok ? "true": "false");
    }

    if (memchr(argv[offset], CHAR_SINGLE, slen)) {
        libinjection_sqli_fingerprint(&sf, argv[offset], slen,
                                      CHAR_SINGLE, COMMENTS_ANSI);
        ok = libinjection_is_sqli_pattern(&sf, NULL);
        fprintf(stdout, "single-ansi\t%s\t%s\n", sf.pat, ok ? "true": "false");
    }

    if (sf.stats_comment_ddx) {
        if (memchr(argv[offset], CHAR_SINGLE, slen)) {
            libinjection_sqli_fingerprint(&sf, argv[offset], slen,
                                          CHAR_SINGLE, COMMENTS_MYSQL);
            ok = libinjection_is_sqli_pattern(&sf, NULL);
            fprintf(stdout, "single-mysql\t%s\t%s\n", sf.pat, ok ? "true": "false");
        }
    }

    if (memchr(argv[offset], CHAR_DOUBLE, slen)) {
        libinjection_sqli_fingerprint(&sf, argv[offset], slen,
                                      CHAR_DOUBLE, COMMENTS_MYSQL);
        ok = libinjection_is_sqli_pattern(&sf, NULL);
        fprintf(stdout, "double-mysql\t%s\t%s\n", sf.pat, ok ? "true": "false");
    }

    return 0;
}
