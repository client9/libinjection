libinjection python API
=================================

The python API follows C API exactly, and you have full access to all
data structures.  It's not that complicated, but it is also not very
pythonic. Future versions of the API will likely include some object
wrapper to make it more simple and prevent bugs.

You should get nearly 400,000 checks per second using the python API.

Install the python module
-------------------------

```
git clone https://github.com/client9/libinjection.git
cd libinjection/python
python setup.py install
```

Note, if for some reason it does work for you, install
[swig](http://www.swig.org), and type <code>make</code>

Using libinjection
--------------------------

```python
from libinjection import *

# create the data object
s = sqli_state()

# initialize it
# last arg should be 0 for now.
astr = "1 UNION ALL SELECT 1"
sqli_init(s, astr, 0)

# check!  return 1 = is sql, 0 is not sqli
issqli = is_sqli(s)

# you might wish to turn it into a bool by doing
# issqli = bool(is_sqli(s))

# if it's true, then you can get the SQLi fingerprint
# by looking in the state object

print s.fingerprint

# reset and do it again
#   again last argument should be 0
astr = "here's a new input"
sqli_reset(s, astr, 0)

is_sqli(s)

```


Warning
----------------------------

This is probably a bug, but for now, the input string must not change
or get destroyed between the `sqli_init` (or `sqli_reset`) call and when
you call `is_sqli`.  While annoying, this prevents libinjection from
having to make an internal copy of the string, which would slow things down.

The following example might crash:

```python
s = sqli_state()

astr = "something"
sqli_init(s, astr, 0)

astr = None

is_sqli(s)
```

Data Structures
----------------------------

The fields in the `libinjection_sqli_token` and `libininjection_sqli_state`
can be accessed in a natural way similar to a python class fields:

```python

s = sqli_state()
s.fingerprint

s = sqli_token()
s.val
```

etc.  There is one exception.  The static C array of
`libinjection_sqli_state.tokenvec` can be accessed used the function
`libinjection_sqli_get_token` which takes a state object and a index, and returns a `struct libinjection_sqli_token*` or a `null` if out of range.

This was done since SWIG seems to have issues with static or fixed
sized arrays in structures (or more likely I don't know how to use
SWIG).   Using the following function simplifies generation of API:

```c
struct libinjection_sqli_token*
libinjection_sqli_get_token(struct libinjection_sqli_state*, int i);
```


Advanced Callbacks
----------------------------

By default, libinjection's SQLi module has a built-in list of
known-sql tokens and known SQLi fingerprints.  Using the callback
functionality, you are able to replace and change this list.

This allows an application to distribute a new SQL token and SQLi
fingerprint list without the end-user doing a full libinjection
upgrade.

Unfortunately, by using the callbacks, the performance drops by over
50%.  Still, it may be useful in some situations.

The current unit-test driver uses this callback, and it's maybe
easiest explaining it with code.

A small program `json2python.py` converts the raw JSON file
containing all the data the C program uses into python.  To
use it:

```
cd libinjection/python
make words.py
```

The output file `words.py` starts like this:

```
import libinjection

def lookup(state, stype, keyword):
    keyword = keyword.upper()
    if stype == libinjection.LOOKUP_FINGERPRINT:
        if keyword in fingerprints and libinjection.sqli_not_whitelist(state):
            return 'F'
        else:
            return chr(0)
    return words.get(keyword, chr(0))
```

The input is:

* `sqli_state` object
* a lookup type.  The only value that matter is `libinjection.LOOKUP_FINGERPRINT`
* the word to look-up

The output is a string of length 1 (a single character).  If it's "\0" (i.e. `chr(0)`), then
it means "nothing matched" or "not found"

This is likely to change in version 4 of libinjection to be nicer but, today,
this is what it is.

Of note is this line:

```python
if keyword in fingerprints and libinjection.sqli_not_whitelist(state):
```

The C version of the code contains some logic that removes false
positives from a few fingerprint types.  You can reuse this logic in
python by calling `sqli_not_whitelist` which returns `true` if it's
SQLi.  For more control, it is best to re-implement this logic in
python (and it is probably faster too).

Also, if your callback raises exceptions or doesn't follow the
API exactly, python is likely to crash.
