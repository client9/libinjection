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

#include "sqlparse.h"

static void replaceAll(std::string& str,
                       const std::string& from,
                       const std::string& to)
{
    size_t start_pos = 0;

    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // ...
    }
}

static string normalize(string s)
{
    // convert '+' to ' ', convert %XX to char
    modp::url_decode(s);
    while (1) {
        size_t olen = s.length();
        modp::url_decode_raw(s);
        if (s.length() == olen) {
            break;
        }
    }

    modp::toupper(s);
    replaceAll(s, "&QUOT;", "\"");
    // TBD all &#34 and backtick as well?
    replaceAll(s, "&#39;", "'");
    return s;
}

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
    qsiter_t qsi;
    size_t pos;
    string orig(argv[offset]);
    switch (itype) {
    case 0:
        pos = orig.find('?');
        if (pos == string::npos) {
            return 0;
        }
        orig = orig.substr(pos + 1);
        // FALL THROUGH
    case 1:
        qsiter_reset(&qsi, orig.data(), orig.size());
        while (qsiter_next(&qsi)) {
            string key(qsi.key, qsi.keylen);
            string val(qsi.val, qsi.vallen);
            string tmp(normalize(val));
            if (is_sqli(&sf, tmp.c_str(), tmp.size())) {
                cout << sf.pat << "\t" << key << "\t" << modp::toprint(tmp) << "\n";
                return 0;
            }
        }
        break;
    case 2:
        string newline(normalize(argv[offset]));
        bool issqli = is_sqli(&sf, newline.c_str(), newline.size());
        if (issqli) {
            cout << sf.pat << "\t" << "\t" << modp::toprint(newline) << "\n";
        }
    }
    return 0;
}
