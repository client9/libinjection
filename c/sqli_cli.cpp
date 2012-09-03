/**
 * Copyright 2012, Nick Galbreath
 * nickg@client9.com
 * GPL v2 License -- Commericial Licenses available.
 *
 *
 * This is for testing against files in ../data/ *.txt
 * Reads from stdin or a list of files, and emits if a line
 * is a SQLi attack or not, and does basic statistics
 *
 */
#include <iostream>
#include <string>
using namespace std;

#include "modp_burl.h"
#include "modp_ascii.h"
#include "modp_qsiter.h"

#include "sqlparse_private.h"


int main(int argc, const char* argv[])
{
    int offset = 1;
    int itype = 2;

    if (argc > 2) {

        if (!strcmp(argv[1], "-u")) {
            // URL
            itype = 0;
            offset += 1;
        } else if (!strcmp(argv[1], "-q")) {
            // query string (no initial '?')
            itype = 1;
            offset += 1;
        } else if (!strcmp(argv[1], "-d")) {
            // direct user input
            itype = 2;
            offset += 1;
        }
    }

    sfilter sf;
    stoken_t current;

    string tmp(argv[offset]);
    modp::toupper(tmp);

    sfilter_reset(&sf, tmp.data(), tmp.size());

    while (sqli_tokenize(&sf, &current)) {
        cout << current.type << " " << current.val << "\n";
    }

    return 0;
}
