/**
 * Copyright 2012, Nick Galbreath
 * nickg@client9.com
 * GPL v2 License -- Commericial Licenses available.
 *
 * (setq-default indent-tabs-mode nil)
 * (setq c-default-style "k&r"
 *     c-basic-offset 4)
 *  indent -kr -nut
 */

#ifndef _SQLPARSE_H
#define _SQLPARSE_H

/*
 * These are done to prevent editors from being confusing by
 * opening "{" and indenting the whole file
 */

#ifdef __cplusplus
#define CPP_START extern "C" {
#define CPP_END }
#else
#define CPP_START
#define CPP_END
#endif

// props to http://sourcefrog.net/weblog/software/languages/C/unused.html

#ifdef UNUSED
#elif defined(__GNUC__)
# define UNUSED(x) UNUSED_ ## x __attribute__((unused))
#elif defined(__LCLINT__)
# define UNUSED(x) /*@unused@*/ x
#else
# define UNUSED(x) x
#endif

CPP_START
#define ST_MAX_SIZE 31
#define MAX_TOKENS 5

typedef struct {
    char type;
    char val[ST_MAX_SIZE];
} stoken_t;

typedef struct {
    /* input */
    const char *s;
    size_t slen;

    /* current tokenize state */
    size_t pos;

    /* syntax fixups state */
    stoken_t syntax_current;
    stoken_t syntax_last;
    stoken_t syntax_comment;

    /* constant folding state */
    stoken_t fold_current;
    stoken_t fold_last;
    int fold_state;

    /* final sqli data */
    stoken_t tokenvec[MAX_TOKENS];

    // +1 for possible ending null
    char pat[MAX_TOKENS + 1];
    char delim;
    int reason;
} sfilter;

void sfilter_reset(sfilter * sf, const char *s, size_t slen);

size_t qs_normalize(char *s, size_t slen);

bool is_sqli(sfilter * sql_state, const char *s, size_t slen);

CPP_END
#endif /* _SQLPARSE_H */
