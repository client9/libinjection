/**
 * Copyright 2012, 2013, 2014 Nick Galbreath
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
#include <assert.h>

#include "libinjection_html5.h"
#include "libinjection_xss.h"
#include "libinjection.h"

const char* h5_type_to_string(enum html5_type x)
{
    switch (x) {
    case DATA_TEXT: return "DATA_TEXT";
    case TAG_NAME_OPEN: return "TAG_NAME_OPEN";
    case TAG_NAME_CLOSE: return "TAG_NAME_CLOSE";
    case TAG_NAME_SELFCLOSE: return "TAG_NAME_SELFCLOSE";
    case TAG_DATA: return "TAG_DATA";
    case TAG_CLOSE: return "TAG_CLOSE";
    case ATTR_NAME: return "ATTR_NAME";
    case ATTR_VALUE: return "ATTR_VALUE";
    case TAG_COMMENT: return "TAG_COMMENT";
    case DOCTYPE: return "DOCTYPE";
    default:
        assert(0);
    }
}

void print_html5_token(h5_state_t* hs)
{
    char* tmp = (char*) malloc(hs->token_len + 1);
    memcpy(tmp, hs->token_start, hs->token_len);
    /* TODO.. encode to be printable */
    tmp[hs->token_len] = '\0';

    printf("%s,%d,%s\n",
	   h5_type_to_string(hs->token_type),
	   (int) hs->token_len,
	   tmp);

    free(tmp);
}

int main(int argc, const char* argv[])
{
    size_t slen;
    h5_state_t hs;
    char* copy;
    int offset = 1;
    int flag = 0;

    if (argc < 2) {
        fprintf(stderr, "need more args\n");
        return 1;
    }

    while (offset < argc) {
      if (strcmp(argv[offset], "-f") == 0) {
            offset += 1;
            flag = atoi(argv[offset]);
            offset += 1;
      } else {
	break;
      }
    }

    /* ATTENTION: argv is a C-string, null terminated.  We copy this
     * to it's own location, WITHOUT null byte.  This way, valgrind
     * can see if we run past the buffer.
     */

    slen = strlen(argv[offset]);
    copy = (char* ) malloc(slen);
    memcpy(copy, argv[offset], slen);


    libinjection_h5_init(&hs, copy, slen, flag);
    while (libinjection_h5_next(&hs)) {
        print_html5_token(&hs);
    }

    if (libinjection_is_xss(copy, slen, flag)) {
      printf("is injection!\n");
    }
    free(copy);
    return 0;
}
