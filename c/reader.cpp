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

class LineIterator {
private:
    const string fname;
    istream& myfile;
    int linenum;
    string line;

public:
  LineIterator(istream& is, const char* filename)
        : fname(filename), myfile(is), linenum(0)
        {

        }

  LineIterator(istream& is, const string& filename)
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
      while (/*myfile.is_open() && */ myfile.good()) {
            linenum +=1;
            getline(myfile, line);
            if (line.length() > 0 && line.at(0) != '#') {
                return true;
            }
        }
        return false;
    }
};

#include "modp_burl.h"
#include "modp_ascii.h"

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

  void test_positive(istream& is, const char* fname) {

      LineIterator li(is, fname);
      sfilter sf;

        while (li.next()) {
            string newline(normalize(li.getLine()));

            //cout << fname << "\t"
            //     << li.getLinenum() << "\t" << newline << "\t";

            bool issqli = is_sqli(&sf, newline.c_str(), newline.size());
            //bool issqli = false;
            if (issqli) {
                test_ok += 1;
                //cout << li.getLinenum() << ": " << newline << "\n";
                cout << fname << "\t"
                     << std::dec << li.getLinenum() << "\tTrue\t"
                     << sf.pat << "\t"
                     << std::dec << pat2int(sf.pat) << "\t"
                     << std::dec << "0" << "\t"
                     << modp::toprint(newline)
                     << "\n";
            } else {
                test_fail += 1;
                cout << fname << "\t"
                     << std::dec << li.getLinenum() << "\tFalse\t"
                     << sf.pat << "\t"
                     << std::dec << pat2int(sf.pat) << "\t"
                     << std::dec << sf.reason << "\t"
                     << modp::toprint(newline)
                     << "\n";
            }
        }
    }

};


int main( int argc, const char* argv[] ) {
    tester atest;
    bool invert = false;


    if (argc == 1) {
      atest.test_positive(cin, "stdin");
    } else if (argc == 2 && (strcmp(argv[1], "-i") == 0)) {
      invert = true;
      atest.test_positive(cin, "stdin");
    } else {
      int offset = 1;

      if (strcmp(argv[1], "-i") == 0) {
        offset = 2;
        invert = true;
      }

      for (int i = offset; i < argc; ++i) {
	ifstream is(argv[i]);
        atest.test_positive(is, argv[i]);
      }
    }

    cerr << "SQLI  : " << atest.test_ok << "\n";
    cerr << "SAFE  : " << atest.test_fail << "\n";
    cerr << "TOTAL : " << atest.test_ok + atest.test_fail << "\n";

    // error codes aren't > 127, else it wraps around
    if (invert) {
        // e.g. NOT sqli
      return (atest.test_ok > 127) ? 127 : atest.test_ok;
    } else {
      // SQLI
      return (atest.test_fail > 127) ? 127 : atest.test_fail;
    }
}
