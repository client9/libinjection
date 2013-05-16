#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include "modp_burl.h"

#include "libinjection.h"

static int g_test_ok = 0;
static int g_test_fail = 0;

void modp_toprint(char* str, size_t len)
{
    size_t i;
    for (i = 0; i < len; ++i) {
        if (str[i] < 32 || str[i] > 126) {
            str[i] = '?';
        }
    }
}
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
size_t modp_xml_encode(char* dest, const char* src, size_t len)
{
    size_t count = 0;
    const char* srcend = src + len;
    char ch;
    while (src < srcend) {
        ch = *src++;
        switch (ch) {
        case '&':
            *dest++ = '&';
            *dest++ = 'a';
            *dest++ = 'm';
            *dest++ = 'p';
            *dest++ = ';';
            count += 5; /* &amp; */
            break;
        case '<':
            *dest++ = '&';
            *dest++ = 'l';
            *dest++ = 't';
            *dest++ = ';';
            count += 4; /* &lt; */
            break;
        case '>':
            *dest++ = '&';
            *dest++ = 'g';
            *dest++ = 't';
            *dest++ = ';';
            count += 4; /* &gt; */
            break;
        case '\'':
            *dest++ = '&';
            *dest++ = 'q';
            *dest++ = 'u';
            *dest++ = 'o';
            *dest++ = 't';
            *dest++ = ';';
            count += 6; /* &quot; */
            break;
        case '\"':
            *dest++ = '&';
            *dest++ = 'a';
            *dest++ = 'p';
            *dest++ = 'o';
            *dest++ = 's';
            *dest++ = ';';
            count += 6; /* &apos; */
            break;
        default:
            *dest++ = ch;
            count += 1;
        }
    }
    *dest = '\0';
    return count;
}

void test_positive(FILE * fd, const char *fname,
                   bool flag_invert, bool output_xml, bool flag_quiet, bool flag_true)
{
    char linebuf[8192];
    char linecopy[8192];

    /**
     * xml-escaped version of sqlifingerprint
     */
    char patxml[128];

    int linenum = 0;
    sfilter sf;

    while (fgets(linebuf, sizeof(linebuf), fd)) {
        linenum += 1;
        size_t len = modp_rtrim(linebuf, strlen(linebuf));
        if (len == 0) {
            continue;
        }
        if (linebuf[0] == '#') {
            continue;
        }

        len =  modp_burl_decode(linebuf, linebuf, len);
        bool issqli = libinjection_is_sqli(&sf, linebuf, len, NULL, NULL);
        if (issqli) {
            g_test_ok += 1;
        } else {
            g_test_fail += 1;
        }

        if (flag_quiet) {
            continue;
        }


        if (output_xml) {
            modp_toprint(linebuf, len);
            modp_xml_encode(linecopy, linebuf, len);
            modp_xml_encode(patxml, sf.pat, strlen(sf.pat));
            if (!issqli && !flag_invert) {
                /*
                 * false negative
                 * did NOT detect a SQLI
                 */

                fprintf(stdout,
                        "<error file=\"%s\" line=\"%d\" id=\"%s\" severity=\"%s\" msg=\"%s\"/>\n",
                        fname, linenum, patxml, "error", linecopy);
            } else if (output_xml && issqli && flag_invert) {
                /*
                 * false positive
                 * incorrect marked a benign input as SQLi
                 */
                fprintf(stdout,
                        "<error file=\"%s\" line=\"%d\" id=\"%s\" severity=\"%s\" msg=\"%s\"/>\n",
                        fname, linenum, patxml, "error", linecopy);
            }
        } else {
            if ((issqli && flag_true) ||
                (!issqli && flag_true && flag_invert) ||
                !flag_true) {
                modp_toprint(linebuf, len);

                fprintf(stdout, "%s\t%d\t%s\t%s\t%d\t%s\n",
                        fname, linenum,
                        (issqli ? "True" : "False"), sf.pat, sf.reason, linebuf);
            }
        }
    }
}

int main(int argc, const char *argv[])
{
    /*
     * invert output, by
     */
    bool flag_invert = false;
    /*
     * xml output for jenkins, etc
     */
    bool flag_xml = false;
    /*
     * only print results
     */
    bool flag_quiet = false;
    /*
     * only print postive results
     * with invert, only print negative results
     */
    bool flag_true = false;

    int flag_slow = 1;

    int i, j;
    int offset = 1;

    while (offset < argc) {
        if (strcmp(argv[offset], "-i") == 0) {
            offset += 1;
            flag_invert = true;
        } else if (strcmp(argv[offset], "-x") == 0) {
            offset += 1;
            flag_xml = true;
        } else if (strcmp(argv[offset], "-q") == 0) {
            offset += 1;
            flag_quiet = true;
        } else if (strcmp(argv[offset], "-t") == 0) {
            offset += 1;
            flag_true = true;
        } else if (strcmp(argv[offset], "-s") == 0) {
            offset += 1;
            flag_slow = 100;
        } else {
            break;
        }
    }

    if (flag_xml && ! flag_quiet) {
        fprintf(stdout, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        fprintf(stdout, "<results>\n");
    }

    if (offset == argc) {
        test_positive(stdin, "stdin", flag_invert, flag_xml, flag_quiet, flag_true);
    } else {
        for (j = 0; j < flag_slow; ++j) {
            for (i = offset; i < argc; ++i) {
                FILE* fd = fopen(argv[i], "r");
                if (fd) {
                    test_positive(fd, argv[i], flag_invert, flag_xml, flag_quiet, flag_true);
                    fclose(fd);
                }
            }
        }
    }

    if (flag_xml && ! flag_quiet) {
        fprintf(stdout, "</results>\n");
    }

    if (! flag_quiet) {
        fprintf(stderr, "SQLI  : %d\n", g_test_ok);
        fprintf(stderr, "SAFE  : %d\n", g_test_fail);
        fprintf(stderr, "TOTAL : %d\n", g_test_ok + g_test_fail);
    }

    return 0;
}
