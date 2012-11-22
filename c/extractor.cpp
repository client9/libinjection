/*
 * Simple program to extract "interesting" query strings
 * values from HTTP log files or other types of logs
 * Not really for prime-time.
 *
 */
#include <iostream>
#include <fstream>
#include <string>

#include "modp_burl.h"
#include "modp_ascii.h"
#include "modp_qsiter.h"

#include "sqli_normalize.h"
#include "sqli_fingerprints.h"
#include "sqlparse.h"

using namespace std;

static bool is_special(std::string& str) {
    string nval(str);
    size_t len = sqli_qs_normalize(const_cast<char*>(nval.data()), nval.size());
    nval.erase(len, std::string::npos);
    //  / *
    if (string::npos == nval.find_first_not_of("ABCDEFGHIJKLMNOPQRSTUVWXYZ _-+")) {
        // all alpha, a few symbols can't be string
        return false;
    } else if (string::npos == nval.find_first_not_of("0123456789. ()[]{}_-+:;,")) {
        // all numbers and random symbols
        return false;
    } else if (string::npos == nval.find_first_not_of("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-+:;,")) {
        // big blobs of text without whitespace
        return false;
    } else {
        return true;
    }
}

class LineIterator {
private:
    const string fname;
    istream* myfile;
    int linenum;
    string line;

public:
    LineIterator(const char* filename, istream* is)
        : fname(filename), myfile(is), linenum(0)
        {

        }

    LineIterator(const string& filename, istream* is)
        : fname(filename), myfile(is), linenum(0)
        {

        }

    const string& getFilename() {
        return this->fname;
    }

    int getLinenum() {
        return this->linenum;
    }

    const string& getLine() {
        return this->line;
    }

    bool next() {
        while (myfile->good()) {
            linenum +=1;
            getline(*myfile, line);
            if (line.length() > 0 && line.at(0) != '#') {
                return true;
            }
        }
        return false;
    }
};


class tester {

public:
    tester()
        {
        }

    void test_positive(const char* fname, istream* is)  {
        sfilter sf;

        bool invert = false;

        LineIterator li(fname, is);

        qsiter_t qsi;

        while (li.next()) {
            string orig(li.getLine());
            if (false) {
                // LOG FILE MODE
                size_t pos = orig.find("GET ");
                if (pos == string::npos) {
                    pos = orig.find("POST ");
                    if (pos == string::npos) {
                        continue;
                    } else {
                        pos += 5;
                    }
                } else {
                    pos += 4;
                }
                size_t endpos = orig.find(' ', pos);
                if (endpos == string::npos) {
                    continue;
                }

                pos = orig.find('?', pos);
                if (pos == string::npos || pos > endpos) {
                    continue;
                }
                pos += 1;

                qsiter_reset(&qsi, orig.data() + pos, endpos-pos);
                bool issqli = false;
                while (!issqli && qsiter_next(&qsi)) {
                    string val(qsi.val, qsi.vallen);
                    string tmp(val);
                    tmp.erase(sqli_qs_normalize(const_cast<char*>(tmp.data()), tmp.size()), std::string::npos);
                    issqli = is_sqli(&sf, tmp.data(), tmp.size(), is_sqli_pattern);
                }
                if (issqli) {
                    cout << orig << "\n";
                }
            } else if (true) {
                bool issqli = false;
                string tmp(orig);
                // RAW MODE -- line is full input to be evalutated.
                if (is_special(orig)) {
                    if (invert) {
                        //
                    } else {
                        tmp.erase(sqli_qs_normalize(const_cast<char*>(tmp.data()), tmp.size()), std::string::npos);
                        issqli = is_sqli(&sf, tmp.data(), tmp.size(), is_sqli_pattern);
                        //cout << tmp << "    |    " << orig << endl;
                        //cout << orig << endl;
                    }
                } else {
                    if (invert) {
                        cout << orig << endl;
                    } else {
                        //
                    }
                }
                if (issqli) {
                    cout << tmp << "\n";
                }
            }
        } /* while li.next() */
    } /* tester */
}; /* class */


int main( int argc, const char* argv[] ) {
    tester atest;

    if (argc == 1) {
        atest.test_positive("stdin", &(cin));
    } else {
        for (int i = 2; i < argc; ++i) {
            ifstream is(argv[i]);
            atest.test_positive(argv[1], &is);
        }
    }

    return 0;
}
