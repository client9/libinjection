
#include "sqlparse_private.h"
#include "sqlparse_data.h"
#include <time.h>

#include <cxxtest/TestSuite.h>
#include <string>
using std::string;
using std::cout;

class MyTestSuite : public CxxTest::TestSuite
{
public:

    void testCreateDelete(void)
        {
            stoken_t* st = st_new();
            st_clear(st);
            TS_ASSERT(st_is_empty(st));
            st_assign_cstr(st, 'o', "FOO");
            TS_ASSERT(!st_is_empty(st));
            st_destroy(&st);

        }

    /**
     * test parsing of '#' eol comment
     */
    void testParsePound(void)
        {
            stoken_t st;

            {
                st_clear(&st);
                const char* s = "#";
                string expected(s);
                size_t pos = parse_eol_comment(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 1);
            }

            {
                st_clear(&st);
                const char* s = "# FOO";
                string expected(s);
                size_t pos = parse_eol_comment(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 5);
            }

            {
                st_clear(&st);
                const char* s = "# FOO\nSELECT";
                string expected("# FOO");
                size_t pos = parse_eol_comment(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 6);
            }

            {
                st_clear(&st);
                const char* s = "BAR # FOO\nSELECT";
                string expected("# FOO");
                size_t pos = parse_eol_comment(s, strlen(s), 4, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 10);
            }
        }

    /** Test "/" division operator
     * "slash star" comments tested elsewhere.
     */
    void testParseSlash(void)
        {
            stoken_t st;

            {
                st_clear(&st);
                const char* s = "/";
                string expected(s);
                size_t pos = parse_slash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'o');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 1);
            }

            {
                st_clear(&st);
                const char* s = "/X";
                string expected("/");
                size_t pos = parse_slash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'o');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 1);
            }

            {
                st_clear(&st);
                const char* s = "/*";
                string expected("/*");
                size_t pos = parse_slash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 2);
            }

            {
                st_clear(&st);
                const char* s = "/* ";
                string expected("/* ");
                size_t pos = parse_slash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 3);
            }

            {
                st_clear(&st);
                const char* s = "/* ABC */";
                string expected("/* ABC */");
                size_t pos = parse_slash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 9);
            }

            {
                st_clear(&st);
                const char* s = " /* ABC */ ";
                string expected("/* ABC */");
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 10);
            }

            {
                // mysql comment /*! is just ignored
                st_clear(&st);
                const char* s = " /*! ABC */ ";
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 4);
            }

            {
                // mysql comment but doesn't matter
                st_clear(&st);
                const char* s = "/*!";
                string expected("/*!");
                size_t pos = parse_slash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 3);
            }

            {
                // mysql comment but doesn't matter
                st_clear(&st);
                const char* s = " /*!0";
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 5);
            }

            {
                // mysql comment but doesn't matter
                st_clear(&st);
                const char* s = "/*!0 ABC";
                size_t pos = parse_slash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 4);
            }

            {
                // mysql comment but doesn't matter
                st_clear(&st);
                const char* s = " /*!00000";
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 9);
            }

            {
                // mysql comment
                st_clear(&st);
                const char* s = " /*!00000 ABC";
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 9);
            }

            {
                // mysql comment
                st_clear(&st);
                const char* s = " /*!0SELECT";
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 5);
            }

            {
                // mysql comment /*! is just ignored
                st_clear(&st);
                const char* s = " /*! ABC ";
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 4);
            }

            // not quite sure what right behavior is
            {
                // mysql comment
                st_clear(&st);
                const char* s = " /*!00 ABC";
                size_t pos = parse_slash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 4);
            }
        }

    void testParseWord(void) {
        stoken_t st;

        {
            st_clear(&st);
            const char* s = " DOODLE ";
            string expected("DOODLE");
            size_t pos = parse_word(s, strlen(s), 1, &st);
            TS_ASSERT_EQUALS(st.type, 'n');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 7);
        }

        {
            st_clear(&st);
            const char* s = " SELECT ";
            string expected("SELECT");
            size_t pos = parse_word(s, strlen(s), 1, &st);
            TS_ASSERT_EQUALS(st.type, 'k');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 7);
        }

        {
            st_clear(&st);
            const char* s = " MAX( ";
            string expected("MAX");
            size_t pos = parse_word(s, strlen(s), 1, &st);
            TS_ASSERT_EQUALS(st.type, 'f');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 4);
        }

        {
            st_clear(&st);
            const char* s = " DIV ";
            string expected("DIV");
            size_t pos = parse_word(s, strlen(s), 1, &st);
            TS_ASSERT_EQUALS(st.type, 'o');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 4);
        }
    }

    void testParseNumber(void) {
        stoken_t st;

        {
            st_clear(&st);
            const char* s = "1";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 1);
        }

        {
            st_clear(&st);
            const char* s = "10";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 2);
        }

        {
            st_clear(&st);
            const char* s = "10";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, strlen(s));
        }

        {
            st_clear(&st);
            const char* s = "1.234567";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, strlen(s));
        }

        {
            st_clear(&st);
            const char* s = ".234567";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, strlen(s));
        }

        {
            st_clear(&st);
            const char* s = "0X0123456789ABCDEF";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, strlen(s));
        }

        {
            st_clear(&st);
            const char* s = "0X";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, 'n');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, strlen(s));
        }

        {
            st_clear(&st);
            const char* s = "1E+10";
            string expected("1E+10");
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 5);
        }

        {
            st_clear(&st);
            const char* s = "1E-10";
            string expected("1E-10");
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 5);
        }

        {
            st_clear(&st);
            const char* s = "1E10";
            string expected("1E10");
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 4);
        }

        {
            st_clear(&st);
            const char* s = "0";
            string expected("0");
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, '1');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 1);
        }

        {
            st_clear(&st);
            const char* s = ".";
            string expected(s);
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, 'n');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, strlen(s));
        }

        {
            st_clear(&st);
            const char* s = ". ";
            string expected(".");
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, 'n');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 1);
        }

        {
            st_clear(&st);
            const char* s = "6FOO ";
            string expected("6FOO");
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, 'n');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 4);
        }

        {
            st_clear(&st);
            const char* s = "4FOO2YOU ";
            string expected("4FOO2YOU");
            size_t pos = parse_number(s, strlen(s), 0, &st);
            TS_ASSERT_EQUALS(st.type, 'n');
            TS_ASSERT_EQUALS(st.val, expected);
            TS_ASSERT_EQUALS(pos, 8);
        }
    }

    /**
     * Test binary search algorithm for 2-char operator lookup
     */
    void testIsOperator2(void)
        {
            {
                const char* op = "+=";
                TS_ASSERT(is_operator2(op));

            }

            {
                const char* op = "XX";
                TS_ASSERT(!is_operator2(op));
            }
        }

    /**
     * Is token english-like
     */
    void testIsEnglishOperator(void)
        {
            stoken_t st;
            {
                st_assign_cstr(&st, 'o', "AND");
                TS_ASSERT(st_is_english_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "&");
                TS_ASSERT(st_is_english_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "NOT");
                TS_ASSERT(st_is_english_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "UNION");
                TS_ASSERT(st_is_english_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "IS");
                TS_ASSERT(st_is_english_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "MOD");
                TS_ASSERT(st_is_english_op(&st));
            }

            {
                st_assign_cstr(&st, 'c', "FOO");
                TS_ASSERT(! st_is_english_op(&st));
            }
            {
                st_assign_cstr(&st, 'c', "MOD");
                TS_ASSERT(! st_is_english_op(&st));
            }
        }

    /**
     * Is token a logical operator
     */
    void testIsUnaryOperator(void)
        {
            stoken_t st;
            {
                st_assign_cstr(&st, 'o', "+");
                TS_ASSERT(st_is_unary_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "-");
                TS_ASSERT(st_is_unary_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "!");
                TS_ASSERT(st_is_unary_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "~");
                TS_ASSERT(st_is_unary_op(&st));
            }

            {
                st_assign_cstr(&st, 'c', "!");
                TS_ASSERT(! st_is_unary_op(&st));
            }

            {
                st_assign_cstr(&st, 'o', "++");
                TS_ASSERT(! st_is_unary_op(&st));
            }
        }


    /**
     * Test binary search algorithm for keyword lookup
     */
    void testGetKeyword(void)
        {
            {
                const char* op = "FOOBAR";
                TS_ASSERT_EQUALS(CHAR_NULL, bsearch_keyword_type(op, sql_keywords, sql_keywords_sz));

            }

            {
                const char* op = "SELECT";
                TS_ASSERT_EQUALS('k', bsearch_keyword_type(op, sql_keywords, sql_keywords_sz));
            }

            {
                const char* op = "COS";
                TS_ASSERT_EQUALS('f', bsearch_keyword_type(op, sql_keywords, sql_keywords_sz));
            }

            {
                const char* op = "UNION";
                TS_ASSERT_EQUALS('U',  bsearch_keyword_type(op, sql_keywords, sql_keywords_sz));
            }
        }

    void testParseString(void)
        {
            stoken_t st;
            {
                st_clear(&st);
                const char* s = "'foo' ";
                string expected("'foo'");
                size_t pos = parse_string(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 's');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 5);
            }

            // extra check, for math errors
            {
                st_clear(&st);
                const char* s = " 'foo' ";
                string expected("'foo'");
                size_t pos = parse_string(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 's');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 6);
            }

            // unterminated string
            {
                st_clear(&st);
                const char* s = "'foo ";
                string expected("'foo ");
                size_t pos = parse_string(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 's');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 5);
            }

            // escaped quotes
            {
                st_clear(&st);
                const char* s = "'foo\\'bar' ";
                string expected("'foo\\'bar'");
                size_t pos = parse_string(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 's');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 10);
            }

            // paranoid check to make sure we dont run past the bounds
            {
                st_clear(&st);
                const char* s = "'foo\\'";
                string expected("'foo\\'");
                size_t pos = parse_string(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 's');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 6);
            }
        }

    void testIsAithOperator(void)
        {
            stoken_t st;

            st_assign_cstr(&st, 'o', "+");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "-");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "!");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "~");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "%");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "*");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "|");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "&");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "MOD");
            TS_ASSERT(st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "DIV");
            TS_ASSERT(st_is_arith_op(&st));

            // negative case
            st_assign_cstr(&st, 'k', "DIV");
            TS_ASSERT(!st_is_arith_op(&st));

            st_assign_cstr(&st, 'o', "=");
            TS_ASSERT(!st_is_arith_op(&st));

        }

    void testOperator2(void)
        {
            stoken_t st;
            {
                st_clear(&st);
                const char* s = " || ";
                string expected("||");
                size_t pos = parse_operator2(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, '&');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 3);
            }

            {
                st_clear(&st);
                const char* s = " */ ";
                size_t pos = parse_operator2(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, CHAR_NULL);
                TS_ASSERT_EQUALS(pos, 3);
            }

            {
                st_clear(&st);
                const char* s = " |+ ";
                string expected("|");
                size_t pos = parse_operator2(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'o');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 2);
            }

            {
                st_clear(&st);
                const char* s = " |";
                string expected("|");
                size_t pos = parse_operator2(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'o');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 2);
            }

            {
                st_clear(&st);
                const char* s = " <=";
                string expected("<=");
                size_t pos = parse_operator2(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'o');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 3);
            }

            {
                st_clear(&st);
                const char* s = " <=>";
                string expected("<=>");
                size_t pos = parse_operator2(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'o');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 4);
            }
        }

    void testBackSlash(void)
        {
            stoken_t st;
            {
                st_clear(&st);
                const char* s = " \\ ";
                string expected("\\");
                size_t pos = parse_backslash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, '?');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 2);
            }

            {
                st_clear(&st);
                const char* s = " \\N ";
                string expected("NULL");
                size_t pos = parse_backslash(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'k');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 3);
            }
        }

    void testVar(void)
        {
            stoken_t st;
            {
                st_clear(&st);
                const char* s = " @ ";
                string expected("@");
                size_t pos = parse_var(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'v');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 2);
            }

            {
                st_clear(&st);
                const char* s = " @@ ";
                string expected("@@");
                size_t pos = parse_var(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'v');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 3);
            }

            {
                st_clear(&st);
                const char* s = " @@FOO ";
                string expected("@@FOO");
                size_t pos = parse_var(s, strlen(s), 1, &st);
                TS_ASSERT_EQUALS(st.type, 'v');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 6);
            }
        }

    void testIsDash(void)
        {
            stoken_t st;
            {
                st_clear(&st);
                const char* s = "- ";
                string expected("-");
                size_t pos = parse_dash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'o');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 1);
            }

            {
                st_clear(&st);
                const char* s = "--";
                string expected("--");
                size_t pos = parse_dash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 2);
            }

            {
                st_clear(&st);
                const char* s = "-- ABCD";
                string expected("-- ABCD");
                size_t pos = parse_dash(s, strlen(s), 0, &st);
                TS_ASSERT_EQUALS(st.type, 'c');
                TS_ASSERT_EQUALS(st.val, expected);
                TS_ASSERT_EQUALS(pos, 7);
            }

        }

    void testMergeTokens(void) {
        stoken_t st1;
        stoken_t st2;

        {
            st_clear(&st1);
            st_clear(&st2);
            TS_ASSERT(!syntax_merge_words(&st1, &st2));
        }

        {
            // merged token would be too long

            st_clear(&st1);
            st_clear(&st2);

            st_assign_cstr(&st1, 'o', "01234567890123456789");
            st_assign_cstr(&st2, 'o', "abcdefghijklmnopqrstuvwxyz");

            TS_ASSERT(!syntax_merge_words(&st1, &st2));
        }

        {
            // not a merge

            st_clear(&st1);
            st_clear(&st2);

            st_assign_cstr(&st1, 'n', "FOO");
            st_assign_cstr(&st2, 'n', "BAR");

            TS_ASSERT(!syntax_merge_words(&st1, &st2));
        }

        {
            // merge

            st_clear(&st1);
            st_clear(&st2);

            st_assign_cstr(&st1, 'n', "UNION");
            st_assign_cstr(&st2, 'n', "ALL");

            TS_ASSERT(syntax_merge_words(&st1, &st2));
            TS_ASSERT_EQUALS(st1.type, 'U');

            string expected("UNION ALL");
            TS_ASSERT_EQUALS(st1.val, expected);

        }
    }


    /**
     * Helper function to run syntax_fold repeatably
     *
     */
    int run_filter_syntax(sfilter* sql_state)
        {

            int tlen = 0;
            while (tlen < MAX_TOKENS &&
                   sqli_tokenize(sql_state, &(sql_state->tokenvec[tlen]))) {
                sql_state->pat[tlen] = sql_state->tokenvec[tlen].type;
                tlen += 1;
            }

            return tlen;
        }


    /**
     * Helper function to run syntax_fold repeatably
     *
     */
    int run_filter_fold(sfilter* sql_state)
        {

            int tlen = 0;
            while (tlen < MAX_TOKENS &&
                   filter_fold(sql_state, &(sql_state->tokenvec[tlen]))) {
                sql_state->pat[tlen] = sql_state->tokenvec[tlen].type;
                tlen += 1;
            }

            return tlen;
        }

    void testFilterSyntax(void) {
        sfilter sf;

        // test empty
        {
            sfilter_reset(&sf, "", 0);
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(0, len);
        }


        // test single none
        {
            string sql("FOO");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT(st_equals_cstr(&sf.tokenvec[0], 'n', "FOO"));
        }

        // test single none
        {
            string sql("FOO BAR");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'n', "FOO") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'n', "BAR") );
        }

        // test single none, with leading comment
        {
            string sql("/* CRAP */FOO BAR");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'n', "FOO") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'n', "BAR") );
        }

        // test single keyword
        {
            string sql("SELECT");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'k', "SELECT") );
        }


        // test single keyword
        {
            string sql("=");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'o', "=") );
        }

        // test single multiword operator
        {
            string sql("UNION");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'U', "UNION") );
        }

        // test single multiword operator
        {
            string sql("UNION ALL");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'U', "UNION ALL") );
        }

        // test single multiword operator
        {
            string sql("999 UNION ALL");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "999") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'U', "UNION ALL") );
        }

        // test single multiword operator
        {
            string sql("UNION /* FOO */ ALL");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'U', "UNION ALL") );
        }

        // test single multiword operator, but not multi-word
        {
            string sql("UNION FOO");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'U', "UNION") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'n', "FOO") );
        }


        // test single multiword operator, but not multi-word
        {
            string sql("NOT LIKE");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'o', "NOT LIKE") );
        }

        // test single multiword operator, but not multi-word
        {
            string sql("NOT UNION");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'o', "NOT") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'U', "UNION") );
        }

        // useless unary op removed
        {
            string sql("NOT - 1");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'o', "NOT") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], '1', "1") );
        }


        // ending comments are preserved
        {
            string sql("UNION -- FOO");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'U', "UNION") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'c', "-- FOO") );
        }

        // double unary
        {
            string sql("FOO + - BAR");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(3, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'n', "FOO"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "+"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[2], 'n', "BAR"));
        }

        // remove useless unary
        {
            string sql("FOO && - BAR");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_syntax(&sf);
            TS_ASSERT_EQUALS(3, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'n', "FOO"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], '&', "&&"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[2], 'n', "BAR"));
        }

    }

    void testFilterFold(void) {
        sfilter sf;

        // test empty
        {
            sfilter_reset(&sf, "", 0);
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(0, len);
        }

        // strip away leading (
        {
            string sql("(((((((1");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "1"));
        }

        // strip away leading unary
        {
            string sql("-+~!-1");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "1"));
        }


        // constant folding 1
        {
            string sql("1+1");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "1"));
        }

        // constant folding 1
        {
            string sql("1+1 FOO");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "1"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'n', "FOO"));
        }

        // constant folding 1
        {
            string sql("1+1+ ");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "1"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "+"));
        }

        // constant folding 1
        {
            string sql("1+1+ FOO");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(3, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "1"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "+"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[2], 'n', "FOO"));
        }

        // constant folding 1
        {
            string sql("FOO + 1 + 1 + FOO");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(5, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'n', "FOO"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "+"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[2], '1', "1"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[3], 'o', "+"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[4], 'n', "FOO"));
        }

        // constant folding 1
        {
            string sql("FOO + FOO");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(3, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'n', "FOO"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "+"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[2], 'n', "FOO"));
        }

        // constant folding 1
        {
            string sql("=");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(1, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'o', "="));
        }

        // constant folding 1
        {
            string sql("4759=");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "4759"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "="));
        }


        // constant folding 1
        {
            string sql("FOO + (");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(3, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], 'n', "FOO"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "+"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[2], '(', "("));
        }

        // constant folding 1  6607 + (
        {
            string sql("6607 + (");
            sfilter_reset(&sf, sql.c_str(), sql.length());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(3, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "6607"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'o', "+"));
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[2], '(', "("));
        }

        // test single multiword operator
        {
            string sql("-999 UNION ALL");
            sfilter_reset(&sf, sql.c_str(), sql.size());
            int len = run_filter_fold(&sf);
            TS_ASSERT_EQUALS(2, len);
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[0], '1', "999") );
            TS_ASSERT( st_equals_cstr(&sf.tokenvec[1], 'U', "UNION ALL") );
        }

    }
};


//  1
//  1 FOO
//  1 +
//  1 + FOO
//  1 + 1
//  1 + 1 FOO
//
