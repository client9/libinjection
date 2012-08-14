/**
 * Copyright 2012, Nick Galbreath
 * nickg@client9.com
 * GPL v2 License -- Commericial Licenses available.
 *
 *
 * HOW TO USE:
 *
 *   // Normalize query or postvar value
 *   // ATTENTION: this modifies user_string... make copy if that is not ok
 *   size_t new_len = qs_normalize(user_string, user_string_len);
 *
 *   sfilter s;
 *   bool sqli = is_sqli(&s, user_string, new_len);
 *
 *   // That's it!  sfilter s has some data on how it matched or not
 *   // details to come!
 *
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
CPP_START

#include "modp_stdint.h"

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

/**
 * Normalizes input string to prepare for SQLi testing:
 *
 *   repeats url decoding until doesn't change
 *   does html unescaping
 *   upper case (ascii only)
 *
 * This modifies the input string and is ALWAYS smaller than original input
 * Ending NULL is added.
 *
 */
size_t qs_normalize(char *s, size_t slen);

/**
 *
 *
 * \return TRUE if SQLi, FALSE is benign
 */
bool is_sqli(sfilter * sql_state, const char *s, size_t slen);

CPP_END
#endif /* _SQLPARSE_H */
