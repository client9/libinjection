#include <stdio.h>
#include <string.h>
#include "libinjection.h"

int main(int argc, const char* argv[])
{
    const char* input;
    size_t slen;
    struct libinjection_sqli_state state;

    if (argc < 2) {
        fprintf(stderr, "Usage: %s inputstring\n", argv[0]);
        return -1;
    }

    input = argv[1];
    slen = strlen(input);

    libinjection_sqli_init(&state, input, slen, FLAG_NONE);
    int issqli = libinjection_is_sqli(&state);
    if (issqli) {
        printf("sqli with fingerprint of '%s'\n", state.fingerprint);
    } else {
        printf("not sqli\n");
    }
    return issqli;
}
