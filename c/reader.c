
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include "modp_ascii.h"

#include "sqlparse.h"

static int g_test_ok = 0;
static int g_test_fail = 0;

void test_positive(FILE* fd, const char* fname)
{
    char linebuf[4096];
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
        len = qs_normalize(linebuf, len);
        bool issqli = is_sqli(&sf, linebuf, len);
        if (issqli) {
            g_test_ok += 1;
        } else {
            g_test_fail += 1;
        }

        modp_toprint(linebuf, len);

        fprintf(stdout, "%s\t%d\t%s\t%s\t%d\t%s\n",
                fname, linenum,
                (issqli ? "True" : "False"),
                sf.pat,
                sf.reason,
                linebuf);
    }
}

int main(int argc, const char* argv[])
{
    int i;
    bool invert = false;
    FILE *fd;

    if (argc == 1) {
        test_positive(stdin, "stdin");
    } else if (argc == 2 && (strcmp(argv[1], "-i") == 0)) {
        invert = true;
        test_positive(stdin, "stdin");
    } else {
        int offset = 1;

        if (strcmp(argv[1], "-i") == 0) {
            offset = 2;
            invert = true;
        }

        for (i = offset; i < argc; ++i) {
            fd = fopen(argv[i], "r");
            if (fd) {
                test_positive(fd, argv[i]);
                fclose(fd);
            }
        }
    }

    fprintf(stderr, "SQLI  : %d\n", g_test_ok);
    fprintf(stderr, "SAFE  : %d\n", g_test_fail);
    fprintf(stderr, "TOTAL : %d\n", g_test_ok + g_test_fail);

    // error codes aren't > 127, else it wraps around
    if (invert) {
        // e.g. NOT sqli
        return (g_test_ok > 127) ? 127 : g_test_ok;
    } else {
        // SQLI
        return (g_test_fail > 127) ? 127 : g_test_fail;
    }
}
