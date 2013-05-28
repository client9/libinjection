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

void print_string(stoken_t* t)
{
    /* print opening quote */
    if (t->str_open != CHAR_NULL) {
        printf("%c", t->str_open);
    }

    /* print content */
    printf("%s", t->val);

    /* print closing quote */
    if (t->str_close != CHAR_NULL) {
        printf("%c", t->str_close);
    }
}

void print_var(stoken_t* t)
{
    if (t->var_count >= 1) {
        printf("%c", '@');
    }
    if (t->var_count == 2) {
        printf("%c", '@');
    }
    print_string(t);
}

void print_token(stoken_t *t) {
    printf("%c ", t->type);
    switch (t->type) {
    case 's':
        print_string(t);
        break;
    case 'v':
        print_var(t);
        break;
    default:
        printf("%s", t->val);
    }
    printf("%s", "\n");
}

int main(int argc, const char* argv[])
{
  char comment_style = COMMENTS_ANSI;
    int fold = 0;
    int detect = 0;

    int i;
    int count;
    int offset = 1;

    sfilter sf;
    stoken_t current;
    if (argc < 2) {
        fprintf(stderr, "need more args\n");
        return 1;
    }
    while (1) {
      if (strcmp(argv[offset], "-m") == 0) {
        comment_style = COMMENTS_MYSQL;
        offset += 1;
      }
      else if (strcmp(argv[offset], "-f") == 0 || strcmp(argv[offset], "--fold") == 0) {
        fold = 1;
        offset += 1;
      } else if (strcmp(argv[offset], "-d") == 0 || strcmp(argv[offset], "--detect") == 0) {
        detect = 1;
        offset += 1;
      } else {
	break;
      }
    }

     /* ATTENTION: argv is a C-string, null terminated.  We copy this
      * to it's own location, WITHOUT null byte.  This way, valgrind
      * can see if we run past the buffer.
      */

    size_t slen = strlen(argv[offset]);
    char* copy = (char* ) malloc(slen);
    memcpy(copy, argv[offset], slen);

    libinjection_sqli_init(&sf, copy, slen, CHAR_NULL, comment_style);
    if (detect == 1) {
      detect = libinjection_is_sqli(&sf, copy, slen, NULL, NULL);
        if (detect) {
            printf("%s\n", sf.pat);
        }
    } else if (fold == 1) {
        count = filter_fold(&sf);
        // printf("count = %d\n", count);
        for (i = 0; i < count; ++i) {
            //printf("token: %d :: ", i);
            print_token(&(sf.tokenvec[i]));
        }
    } else {
        while (libinjection_sqli_tokenize(&sf, &current)) {
            print_token(&current);
        }
    }

    free(copy);

    return 0;
}
