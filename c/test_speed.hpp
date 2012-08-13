
#include "sqlparse_private.h"
#include "sqlparse_data.h"
#include <time.h>

#include <cxxtest/TestSuite.h>
#include <string>
using std::string;

class TestSpeed : public CxxTest::TestSuite
{
public:

    void testParseToken(void)
        {
            const char* s  = "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";

            const size_t slen = strlen(s);
            const int imax = 1000000;
            stoken_t st;
            clock_t t0 = clock();
            for (int i = imax; i != 0; --i) {
                size_t pos = 0;
                while (parse_token(s, slen, &pos, &st, CHAR_NULL)) {
                    //printf("[ %c, %s]\n", st.type, st.val);
                }
            }
            clock_t t1 = clock();
            double total = (double)(t1-t0) / (double)CLOCKS_PER_SEC;
            printf("TPS = %f\n", (double) imax / total);
        }


    void testParseSyntax(void)
        {
            const char* s  = "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";
            const size_t slen = strlen(s);
            const int imax = 1000000;
            stoken_t st;
            sfilter sf;
            clock_t t0 = clock();
            for (int i = imax; i != 0; --i) {
                sfilter_reset(&sf, s, slen);
                while (filter_syntax(&sf, &st)) {
                    //printf("[ %c, %s]\n", st.type, st.val);
                }
            }
            clock_t t1 = clock();
            double total = (double)(t1-t0) / (double)CLOCKS_PER_SEC;
            printf("TPS = %f\n", (double) imax / total);
        }

    void testParseFold(void)
        {
            const char* s  = "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";
            const size_t slen = strlen(s);
            const int imax = 1000000;
            stoken_t st;
            sfilter sf;
            clock_t t0 = clock();
            for (int i = imax; i != 0; --i) {
                sfilter_reset(&sf, s, slen);
                while (filter_fold(&sf, &st)) {
                    //printf("[ %c, %s]\n", st.type, st.val);
                }
            }
            clock_t t1 = clock();
            double total = (double)(t1-t0) / (double)CLOCKS_PER_SEC;
            printf("TPS = %f\n", (double) imax / total);
        }

    void testIsSQL(void)
        {
            const char* s  = "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' \"BAR\" /* BAR */ UNION ALL SELECT (2,3,4) || COS(+0X04) --FOOBAR";
            const size_t slen = strlen(s);
            const int imax = 1000000;
            sfilter sf;
            clock_t t0 = clock();
            for (int i = imax; i != 0; --i) {
                is_sqli(&sf, s, slen);
            }
            clock_t t1 = clock();
            double total = (double)(t1-t0) / (double)CLOCKS_PER_SEC;
            printf("TPS = %f\n", (double) imax / total);
        }

};
