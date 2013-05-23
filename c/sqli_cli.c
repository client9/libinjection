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

/*
 * yeah we are including the whole file
 * we are doing this since some of the functions are 'private'
 * and this way we get access to them
 */
#include "libinjection_sqli.c"


int main(int argc, const char* argv[])
{
    int fold = 0;

    int offset = 1;

    sfilter sf;
    stoken_t current;
    if (argc < 2) {
        fprintf(stderr, "need more args\n");
        return 1;
    }
    if (strcmp(argv[offset], "-f") == 0 || strcmp(argv[offset], "--fold") == 0) {
        fold = 1;
        offset += 1;
    }

     /* ATTENTION: argv is a C-string, null terminated.  We copy this
      * to it's own location, WITHOUT null byte.  This way, valgrind
      * can see if we run past the buffer.
      */

    size_t slen = strlen(argv[offset]);
    char* copy = (char* ) malloc(slen);
    memcpy(copy, argv[offset], slen);

    libinjection_sqli_init(&sf, copy, slen, CHAR_NULL);
    int count;
    if (fold == 1) {
        count = filter_fold(&sf);
        // printf("count = %d\n", count);
        for (int i = 0; i < count; ++i) {
            //printf("token: %d :: ", i);
            if (sf.tokenvec[i].type == 's') {
                printf("%c ", sf.tokenvec[i].type);
                if (sf.tokenvec[i].str_open != CHAR_NULL) {
                    printf("%c", sf.tokenvec[i].str_open);
                }
                printf("%s", sf.tokenvec[i].val);
                if (sf.tokenvec[i].str_close != CHAR_NULL) {
                    printf("%c", sf.tokenvec[i].str_open);
                }
                printf("%s", "\n");
            } else {
                printf("%c %s \n", sf.tokenvec[i].type, sf.tokenvec[i].val);
            }
        }
    } else {
        while (libinjection_sqli_tokenize(&sf, &current)) {
            if (current.type == 's') {
                printf("%c ", current.type);
                if (current.str_open != CHAR_NULL) {
                    printf("%c", current.str_open);
                }
                printf("%s", current.val);
                if (current.str_close != CHAR_NULL) {
                    printf("%c", current.str_open);
               }
                printf("%s", "\n");
            } else {
                printf("%c %s\n", current.type, current.val);
            }
        }
    }

    free(copy);

    return 0;
}
