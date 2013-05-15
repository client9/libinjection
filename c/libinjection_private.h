/**
 * Copyright 2012, 2013 Nick Galbreath
 * nickg@client9.com
 * BSD License - see COPYING.txt for details
 *
 */
#ifndef _LIBINJECTION_PRIVATE_H
#define _LIBINJECTION_PRIVATE_H

#include "libinjection.h"

typedef struct {
    const char *word;
    char type;
} keyword_t;

static size_t parse_money(sfilter * sf);
static size_t parse_other(sfilter * sf);
static size_t parse_white(sfilter * sf);
static size_t parse_operator1(sfilter *sf);
static size_t parse_char(sfilter *sf);
static size_t parse_eol_comment(sfilter *sf);
static size_t parse_dash(sfilter *sf);
static size_t parse_slash(sfilter *sf);
static size_t parse_backslash(sfilter * sf);
static size_t parse_operator2(sfilter *sf);
static size_t parse_string(sfilter *sf);
static size_t parse_word(sfilter * sf);
static size_t parse_var(sfilter * sf);
static size_t parse_number(sfilter * sf);

int parse_token(sfilter * sf);

/**
 * Looks at syntax_last and syntax_current to see
 * if they can be merged into a multi-keyword
 */
int syntax_merge_words(stoken_t * a, stoken_t * b);

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
