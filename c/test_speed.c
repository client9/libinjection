/*
 */
#include <time.h>
#include <string.h>
#include <stdio.h>

#include "sqlparse_private.h"
#include "sqli_fingerprints.h"


void testParseToken(void)
{
    const char *s =
        "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";

    const size_t slen = strlen(s);
    const int imax = 1000000;
    int i;
    sfilter sf;
    clock_t t0 = clock();
    for (i = imax; i != 0; --i) {
        sfilter_reset(&sf, s, slen);
        while (parse_token(&sf)) {
            //printf("[ %c, %s]\n", st.type, st.val);
        }
    }
    clock_t t1 = clock();
    double total = (double) (t1 - t0) / (double) CLOCKS_PER_SEC;
    printf("Raw Tokenization TPS          = %f\n", (double) imax / total);
}


void testParseSyntax(void)
{
    const char *s =
        "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";
    const size_t slen = strlen(s);
    const int imax = 1000000;
    int i;
    stoken_t st;
    sfilter sf;
    clock_t t0 = clock();
    for (i = imax; i != 0; --i) {
        sfilter_reset(&sf, s, slen);
        while (sqli_tokenize(&sf, &st)) {
            /* NOP */
        }
    }
    clock_t t1 = clock();
    double total = (double) (t1 - t0) / (double) CLOCKS_PER_SEC;
    printf("SQLi Tokenize TPS             = %f\n", (double) imax / total);
}

void testParseFold(void)
{
    const char *s =
        "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";
    const size_t slen = strlen(s);
    const int imax = 1000000;
    int i;
    stoken_t st;
    sfilter sf;
    clock_t t0 = clock();
    for (i = imax; i != 0; --i) {
        sfilter_reset(&sf, s, slen);
        while (filter_fold(&sf, &st)) {
            /* NOP */
        }
    }
    clock_t t1 = clock();
    double total = (double) (t1 - t0) / (double) CLOCKS_PER_SEC;
    printf("Tokenize + Folding TPS        = %f\n", (double) imax / total);
}

void testIsSQL(void)
{
    const char *s =
        "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";
    const size_t slen = strlen(s);
    const int imax = 1000000;
    int i;
    sfilter sf;
    clock_t t0 = clock();
    for (i = imax; i != 0; --i) {
        is_sqli(&sf, s, slen, is_sqli_pattern);
    }
    clock_t t1 = clock();
    double total = (double) (t1 - t0) / (double) CLOCKS_PER_SEC;
    printf("IsSQLi TPS                    = %f\n", (double) imax / total);
}

int main()
{
    testParseToken();
    testParseSyntax();
    testParseFold();
    testIsSQL();
    return 0;
}
