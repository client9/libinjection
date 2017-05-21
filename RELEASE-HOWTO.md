# libinjection release howto

##  Update the internal version number

in `src/libinjection_sqli.c` edit the definition

```c
#define LIBINJECTION_VERSION "3.9.1"
```

## run ./tags.sh

This will get the versoin number from the file above and create a local
and remote tag.

## HELP!

I would be great to dump a src tarball on github releases.

