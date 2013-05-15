/*
 */
#include <time.h>
#include <string.h>
#include <stdio.h>

#include "libinjection.h"

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
        libinjection_is_sqli(&sf, s, slen, NULL, NULL);
    }
    clock_t t1 = clock();
    double total = (double) (t1 - t0) / (double) CLOCKS_PER_SEC;
    printf("IsSQLi TPS                    = %f\n", (double) imax / total);
}

int main()
{
    testIsSQL();
    return 0;
}
