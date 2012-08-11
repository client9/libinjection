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

#include "sqlparse.h"

using namespace std;

static void replaceAll(std::string& str, const std::string& from, const std::string& to) {
    size_t start_pos = 0;

    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // ...
    }
}

string normalize(string s) {
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

static bool is_special(std::string& str) {
    string nval(normalize(str));
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
            if (true) {
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
                    string tmp(normalize(val));
                    issqli = is_sqli(&sf, tmp.c_str(), tmp.size());
                }
                if (issqli) {
                    cout << orig << "\n";
                }
            } else if (true) {
                // RAW MODE -- line is full input to be evalutated.
                if (is_special(orig)) {
                    if (invert) {
                        //
                    } else {
                        string tmp(normalize(orig));
                        cout << tmp << "    |    " << orig << endl;
                        //cout << orig << endl;
                    }
                } else {
                    if (invert) {
                        cout << orig << endl;
                    } else {
                        //
                    }
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
