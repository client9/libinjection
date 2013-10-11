#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <glob.h>
#include "libinjection.h"

char g_test[8096];
char g_input[8096];
char g_expected[8096];

size_t modp_rtrim(char* str, size_t len)
{
    while (len) {
        char c = str[len -1];
        if (c == ' ' || c == '\n' || c == '\t' || c == '\r') {
            str[len -1] = '\0';
            len -= 1;
        } else {
            break;
        }
    }
    return len;
}

size_t print_string(char* buf, size_t len, stoken_t* t)
{
    /* print opening quote */
    if (t->str_open != '\0') {
        len += sprintf(buf + len, "%c", t->str_open);
    }

    /* print content */
    len += sprintf(buf + len, "%s", t->val);

    /* print closing quote */
    if (t->str_close != '\0') {
        len += sprintf(buf + len, "%c", t->str_close);
    }

    return len;
}

size_t print_var(char* buf, size_t len, stoken_t* t)
{
    if (t->count >= 1) {
        len += sprintf(buf + len, "%c", '@');
    }
    if (t->count == 2) {
        len += sprintf(buf + len, "%c", '@');
    }
    return print_string(buf, len, t);
}

size_t print_token(char* buf, size_t len, stoken_t *t) {
    len += sprintf(buf + len, "%c ", t->type);
    switch (t->type) {
    case 's':
        len = print_string(buf, len, t);
        break;
    case 'v':
        len = print_var(buf, len, t);
        break;
    default:
        len += sprintf(buf + len, "%s", t->val);
    }
    len += sprintf(buf + len, "%c", '\n');
    return len;
}

int read_file(const char* fname, int flags, int testtype)
{
    int count = 0;
    FILE *fp = NULL;
    char linebuf[8192];
    char g_actual[8192];
    char* bufptr = NULL;
    sfilter sf;
    int ok = 1;
    int num_tokens;
    int issqli;
    int i;

    g_test[0] = '\0';
    g_input[0] = '\0';
    g_expected[0] = '\0';

    fp = fopen(fname, "r");
    while(fgets(linebuf, sizeof(linebuf), fp) != NULL) {
        if (count == 0 && strcmp(linebuf, "--TEST--\n") == 0) {
            bufptr = g_test;
            count = 1;
        } else if (count == 1 && strcmp(linebuf, "--INPUT--\n") == 0) {
            bufptr = g_input;
            count = 2;
        } else if (count == 2 && strcmp(linebuf, "--EXPECTED--\n") == 0) {
            bufptr = g_expected;
            count = 3;
        } else {
            strcat(bufptr, linebuf);
        }
    }
    fclose(fp);
    if (count != 3) {
        return 1;
    }

    g_expected[modp_rtrim(g_expected, strlen(g_expected))] = '\0';
    g_input[modp_rtrim(g_input, strlen(g_input))] = '\0';


    size_t slen = strlen(g_input);
    char* copy = (char* ) malloc(slen);
    memcpy(copy, g_input, slen);
    libinjection_sqli_init(&sf, copy, slen, flags);

    /* just here for code coverage and cppcheck */
    libinjection_sqli_callback(&sf, NULL, NULL);

    slen = 0;
    g_actual[0] = '\0';
    if (testtype == 1) {
        issqli = libinjection_is_sqli(&sf);
        if (issqli) {
            sprintf(g_actual, "%s", sf.fingerprint);
        }
    } else if (testtype == 2) {
        num_tokens = libinjection_sqli_fold(&sf);
        for (i = 0; i < num_tokens; ++i) {
            slen = print_token(g_actual, slen, libinjection_sqli_get_token(&sf, i));
        }
    } else {
        while (libinjection_sqli_tokenize(&sf) == 1) {
            slen = print_token(g_actual, slen, sf.current);
        }
    }

    g_actual[modp_rtrim(g_actual, strlen(g_actual))] = '\0';

    if (strcmp(g_expected, g_actual) != 0) {
        printf("INPUT: \n%s\n==\n", g_input);
        printf("EXPECTED: \n%s\n==\n", g_expected);
        printf("GOT: \n%s\n==\n", g_actual);
        ok = 0;
    }

    free(copy);
    return ok;
}

int main(int argc, char** argv)
{
    int offset = 1;
    int i;
    int ok;
    int count = 0;
    int count_fail = 0;
    int flags = 0;
    int testtype = 0;
    int quiet = 0;

    const char* fname;
    while (1) {
        if (strcmp(argv[offset], "-q") == 0 || strcmp(argv[offset], "--quiet") == 0) {
            quiet = 1;
            offset += 1;
        } else {
            break;
        }
    }

    for (i = offset; i < argc; ++i) {
        fname = argv[i];
        count += 1;
        if (strstr(fname, "test-tokens-")) {
            flags = FLAG_QUOTE_NONE | FLAG_SQL_ANSI;
            testtype = 0;
        } else if (strstr(fname, "test-folding-")) {
            flags = FLAG_QUOTE_NONE | FLAG_SQL_ANSI;
            testtype = 2;
        } else if (strstr(fname, "test-sqli-")) {
            flags = FLAG_NONE;
            testtype = 1;
        } else {
            fprintf(stderr, "Unknown test type: %s, failing\n", fname);
            count_fail += 1;
            continue;
        }

        ok = read_file(fname, flags, testtype);
        if (ok) {
            if (! quiet) {
                fprintf(stderr, "%s: ok\n", fname);
            }
        } else {
            count_fail += 1;
            if (! quiet) {
                fprintf(stderr, "%s: fail\n", fname);
            }
        }
    }
    return count > 0 && count_fail > 0;
}
