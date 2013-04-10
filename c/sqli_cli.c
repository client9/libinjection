/**
 * Copyright 2012, Nick Galbreath
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

#include "modp_ascii.h"
#include "sqlparse_private.h"


int main(int argc, const char* argv[])
{
    int fold = 0;

    int offset = 1;

    sfilter sf;
    stoken_t current;
    if (argc < 2) {
        return 1;
    }
    if (strcmp(argv[offset], "-f") == 0 || strcmp(argv[offset], "--fold") == 0) {
        fold = 1;
        offset += 1;
    }

    size_t slen = strlen(argv[offset]);
    char* copy = (char*) malloc(slen + 1);
    if (copy == NULL) {
        return 1;
    }
    modp_toupper_copy(copy, argv[offset], slen);

    sfilter_reset(&sf, copy, slen);

    if (fold == 1) {
        while (filter_fold(&sf, &current)) {
            printf("%c %s\n", current.type, current.val);
        }
    } else {
        while (sqli_tokenize(&sf, &current)) {
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
