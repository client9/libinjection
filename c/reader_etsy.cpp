
#include <iostream>
#include <fstream>
#include <string>

#include "sqlparse.h"

using namespace std;

static void replaceAll(std::string& str, const std::string& from, const std::string& to) {
    size_t start_pos = 0;

    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // ...
    }
}

#include "modp_burl.h"
#include "modp_ascii.h"
#include "modp_qsiter.h"

string normalize(string s) {

    // convert '+' to ' ', convert %XX to char
    modp::url_decode(s);
    modp::toupper(s);

    while (1) {
        size_t olen = s.length();
        modp::url_decode_raw(s);
        modp::toupper(s);

        if (s.length() == olen) {
            break;
        }
    }

    replaceAll(s, "&QUOT;", "\"");
    // TBD all &#34 and backtick as well?
    replaceAll(s, "&#39;", "'");
    return s;
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
private:

public:
    int test_ok;
    int test_fail;

public:
    tester()
        : test_ok(0), test_fail(0)
        {
        }

    void test_positive(const char* fname, istream* is)  {

        LineIterator li(fname, is);

        sfilter sf;
        qsiter_t qsi;

        while (li.next()) {
            string orig(li.getLine());

            size_t pos = orig.find("GET ");
            if (pos == string::npos) {
                pos = orig.find("POST ");
                if (pos == string::npos) {
                    continue;
                }
            }
            pos = orig.find('?', pos+4);
            if (pos == string::npos) {
                continue;
            }
            pos += 1;
            size_t endpos = orig.find(" ", pos);
            if (endpos == string::npos) {
                continue;
            }

            //cout << li.getLinenum() << "\n";

            //string qs(orig.substr(pos, endpos-pos));
            //cout << "QS = " << qs << "\n";

            qsiter_reset(&qsi, orig.data() + pos, endpos-pos);
            bool issqli = false;
            while (!issqli && qsiter_next(&qsi)) {
                if (qsi.vallen) {
                    //cout << "VALLEN = " << qsi.vallen << "\n";
                    string val(qsi.val, qsi.vallen);
                    //cout << "VALUE = " << val << "\n";

                    string newline(normalize(val));
                    //cout << "NEWVAL " << newline << "\n";
                    issqli = is_sqli(&sf, newline.c_str(), newline.size());
                }
            }
            if (issqli) {
                cout << orig << std::endl;
            }
        } /* while li.next() */
    } /* tester */
}; /* class */


int main( int argc, const char* argv[] ) {
    tester atest;

    if (argc == 1) {
        atest.test_positive("stdin", &(cin));
    } else {
        for (int i = 1; i < argc; ++i) {
            ifstream is(argv[1]);
            atest.test_positive(argv[1], &is);
        }
    }

    cerr << "SQLI  : " << atest.test_ok << "\n";
    cerr << "SAFE  : " << atest.test_fail << "\n";
    cerr << "TOTAL : " << atest.test_ok + atest.test_fail << "\n";

    return 0;
}
