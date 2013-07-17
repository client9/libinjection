#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "libinjection.h"

char g_test[4096];
char g_input[4096];
char g_expected[4096];

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
    char linebuf[4096];
    char g_actual[4096];
    char* bufptr;
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
            slen = print_token(g_actual, slen, &(sf.tokenvec[i]));
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
    int count_ok = 0;
    int count_fail = 0;
    int flags = 0;
    int testtype = 0;

    while (1) {
        if (strcmp(argv[offset], "-f") == 0 || strcmp(argv[offset], "--fold") == 0) {
            testtype = 2;
            offset += 1;
        } else if (strcmp(argv[offset], "-d") == 0 || strcmp(argv[offset], "--detect") == 0) {
            testtype = 1;
            offset += 1;
        } else if (strcmp(argv[offset], "-ca") == 0) {
            flags |= FLAG_SQL_ANSI;
            offset += 1;
        } else if (strcmp(argv[offset], "-cm") == 0) {
            flags |= FLAG_SQL_MYSQL;
            offset += 1;
        } else if (strcmp(argv[offset], "-q0") == 0) {
            flags |= FLAG_QUOTE_NONE;
            offset += 1;
        } else if (strcmp(argv[offset], "-q1") == 0) {
            flags |= FLAG_QUOTE_SINGLE;
            offset += 1;
        } else if (strcmp(argv[offset], "-q2") == 0) {
            flags |= FLAG_QUOTE_DOUBLE;
            offset += 1;
        } else {
            break;
        }
    }

    for (i = offset; i < argc; ++i) {
        count += 1;
        //fprintf(stderr, "%s: ", argv[i]);
        ok = read_file(argv[i], flags, testtype);
        if (ok) {
            count_ok += 1;
            //fprintf(stderr, "ok\n");
        } else {
            count_fail += 1;
            fprintf(stderr, "%s: fail\n", argv[i]);
        }
    }
    return count > 0 && count_fail > 0;
}
