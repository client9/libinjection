/* libinjection.i SWIG interface file for PHP */
%module libinjection
%{
#include "libinjection.h"
%}

%include "typemaps.i"

// The C functions all start with 'libinjection_' as a namespace
// We don't need this since it's in the libinjection python package
// i.e. libinjection.libinjection_is_sqli --> libinjection.is_sqli
//
%rename("%(strip:[libinjection_])s") "";

// automatically append string length into arg array
%apply (char *STRING, size_t LENGTH) { (const char *s, size_t slen) };


%include "libinjection.h"
