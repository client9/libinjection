#include <stdio.h>
#include <string.h>
#include "libinjection.h"

int main(int argc, const char* argv[])
{
    const char* input;
    size_t slen;

    if (argc < 2) {
        fprintf(stderr, "Usage: %s inputstring\n", argv[0]);
        return -1;
    }

    input = argv[1];
    slen = strlen(input);

    char fingerprint[8];

    int issqli = libinjection_sqli(input, slen, fingerprint);
    if (issqli) {
        printf("sqli with fingerprint of '%s'\n", fingerprint);
    } else {
        printf("not sqli\n");
    }


    return issqli;
}
