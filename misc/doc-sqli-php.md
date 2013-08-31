libinjection PHP API
=================================

The libinjection PHP API provides full access to the functions
and data structions of the C API.  It's very low-level and not
very pretty, but it's also very easy to assemble higher level
functionality.

<p><b>
Help wanted on packaging into a PEAR module and help with Mac OS X
</b></p>

Install the PHP module
-------------------------

It should be as simple as:

```
make
```

This produces a `libinjection.so` which can be installed with other
PHP extensions.

To load the module, add the following to your `php.ini` file:

```
extension=/path/to/libinjection.so
```

Or you might be able to do:

```
// note may not work with PHP CLI without other
// configuration changes
dl_open('/path/to/libinjection.so');
```

You can do a quick test with:

```php
echo LIBINJECTION_VERSION . "\n";
```


Using libinjection
-------------------------

The basic flow is as follows:

```php

// create a state object using a special function
// one does not use the 'new operator'
// this object can be reused.
$ss = new_libinjection_sqli_state();

// one URL-decodes the input
// validates and normalizes the UTF-8
$arg = "1 union select 1,2,3,4 --";

// always 0 for now
$flags = 0;

//
// Prepare to do work
//
libinjection_sqli_init($ss, $arg, $flags);

//
// now check if SQLi
// returns
//   0 == safe input
//   1 == is sqli
$issqli = libinjection_is_sqli($ss);

$fingerprint = '';
if ($sqli == 1) {
   $fingerprint = libinjection_sqli_state_fingerprint_get($x);
}

// do something

```

This flow can be wrapped into a simple class:

```

class libinjection {
  public $_cPtr=null;

  function __construct() {
     $this->_cPtr = new_libinjection_sqli_state();
  }
  function is_sqli($arg) {
     libinjection_sqli_init($this->_cPtr, $arg, 0);
     $issqli = libinjection_is_sqli($this->_cPtr);

     $fingerprint = '';
     if ($sqli == 1) {
         $fingerprint = libinjection_sqli_state_fingerprint_get($this->_cPtr);
     }
     return $fingerprint;
  }
};

libinject = new libinjection();

$fingerprint = libinjection.is_sqli("1 union select 2 --");
if ($fingerprint) {
  // do sometjing
}
```


Using libinjection data structures
----------------------------------

The API to the data structure fields isn't pretty but it is easy.
Everything is in the form of `datastructurename-field-get`.  For
example `libinjection_sqli_state_slen_get` or
`libinjection_sqli_token_type_get`.

This is one exception, that is the `tokenvec` in
`libinjection_sqli_state`.  The `swig` doesn't appear to understand
static C arrays.  To access elements, use
`libinjection_sqli_state_tokenvec_geti` and pass in the state object,
and an index value (integer).

All the data structures are also read-only.


