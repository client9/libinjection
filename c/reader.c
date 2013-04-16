#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include "modp_burl.h"
#include "modp_ascii.h"

#include "sqlparse.h"
#include "sqli_fingerprints.h"


static int g_test_ok = 0;
static int g_test_fail = 0;

void test_positive(FILE * fd, const char *fname, bool flag_invert, bool output_xml)
{
    char linebuf[8192];
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
        bool issqli = is_sqli(&sf, linebuf, len, is_sqli_pattern);
        if (issqli) {
            g_test_ok += 1;
        } else {
            g_test_fail += 1;
        }

        modp_toprint(linebuf, len);

        if (output_xml) {
            if (!issqli && !flag_invert) {
            // false negative
            // did NOT detect a SQLI
            fprintf(stdout,
                    "<error file=\"%s\" line=\"%d\" id=\"%s\" severity=\"%s\" msg=\"%s\"/>\n",
                    fname, linenum, "notsqli", "error", linebuf);
            } else if (output_xml && issqli && flag_invert) {
                // false positive
                // incorrect marked a benign input as SQLi
                fprintf(stdout,
                        "<error file=\"%s\" line=\"%d\" id=\"%s\" severity=\"%s\" msg=\"%s\"/>\n",
                        fname, linenum, "sqli", "error", linebuf);
            }
        } else {
            fprintf(stdout, "%s\t%d\t%s\t%s\t%d\t%s\n",
                    fname, linenum,
                    (issqli ? "True" : "False"), sf.pat, sf.reason, linebuf);
        }
    }
}

int main(int argc, const char *argv[])
{
    bool flag_invert = false;
    bool flag_xml = false;
    int i;
    int offset = 1;

    while (offset < argc) {
        if (strcmp(argv[offset], "-i") == 0) {
            offset += 1;
            flag_invert = true;
        } else if (strcmp(argv[offset], "-x") == 0) {
            offset += 1;
            flag_xml = true;
        } else {
            break;
        }
    }

    if (flag_xml) {
        fprintf(stdout, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        fprintf(stdout, "<results>\n");
    }

    if (offset == argc) {
        test_positive(stdin, "stdin", flag_invert, flag_xml);
    } else {
        for (i = offset; i < argc; ++i) {
            FILE* fd = fopen(argv[i], "r");
            if (fd) {
                test_positive(fd, argv[i], flag_invert, flag_xml);
                fclose(fd);
            }
        }
    }

    if (flag_xml) {
        fprintf(stdout, "</results>\n");
    }

    fprintf(stderr, "SQLI  : %d\n", g_test_ok);
    fprintf(stderr, "SAFE  : %d\n", g_test_fail);
    fprintf(stderr, "TOTAL : %d\n", g_test_ok + g_test_fail);

    return 0;
}
