/**
 * Copyright 2012, 2013 Nick Galbreath
 * nickg@client9.com
 * BSD License - see COPYING.txt for details
 *
 */
#ifndef _LIBINJECTION_PRIVATE_H
#define _LIBINJECTION_PRIVATE_H

#include "libinjection.h"

int parse_token(sfilter * sf);

void sfilter_reset(sfilter * sf, const char *s, size_t slen);

/**
 * Takes a raw stream of SQL tokens and does the following:
 * * Merge mutliple strings into one "foo", "bar" --> "foo bar"
 * * Remove comments except last one 1, +, -- foo, 1 ->> 1,+,1
 * * Merge multi-word keywords and operators into one
 *   e.g. "UNION", "ALL" --> "UNION ALL"
 */
int sqli_tokenize(sfilter * sf, stoken_t * sout);

int filter_fold(sfilter * sf, stoken_t * sout);


#endif /* _LIBINJECTION_PRIVATE_H */
