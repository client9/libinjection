/**
 * Copyright 2012, 2013 Nick Galbreath
 * nickg@client9.com
 * BSD License -- see COPYING.txt for details
 *
 *
 * HOW TO USE:
 *
 *   #include "sqlparse.h"
 *
 *   // Normalize query or postvar value
 *   // If it comes in urlencoded, then it's up to you
 *   // to urldecode it.  If it's in correct form already
 *   // then nothing to do!
 *
 *   sfilter s;
 *   int sqli = is_sqli(&s, user_string, new_len, NULL);
 *
 *   // 0 = not sqli
 *   // 1 = is sqli
 *
 *   // That's it!  sfilter s has some data on how it matched or not
 *   // details to come!
 *
 */

#ifndef _SQLPARSE_H
#define _SQLPARSE_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Version info.
 * See python's normalized version
 * http://www.python.org/dev/peps/pep-0386/#normalizedversion
 */
#define LIBINJECTION_VERSION "1.2.0"

#define ST_MAX_SIZE 32
#define MAX_TOKENS 5

#define CHAR_NULL '\0'
#define CHAR_SINGLE '\''
#define CHAR_DOUBLE '"'

typedef struct {
    char type;
    char str_open;
    char str_close;
    char val[ST_MAX_SIZE];
} stoken_t;

typedef struct {
    /* input */
    const char *s;
    size_t slen;

    /* current tokenize state */
    size_t pos;
    int    in_comment;

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

    /*  +1 for ending null */
    char pat[MAX_TOKENS + 1];
    char delim;
    int reason;
} sfilter;

/**
 * Pointer to function, takes cstr input, return true/false
 */
typedef int (*ptr_fingerprints_fn)(const char*);

/**
 * Pointer to function, takes cstr input and callback data, return true/false
 */
typedef int (*ptr_fingerprints2_fn)(const char*, void *);

/**
 * Main API: tests for SQLi in three possible contexts, no quotes,
 * single quote and double quote
 *
 * \param sql_state
 * \param s
 * \param slen
 * \param fn a pointer to a function that determines if a fingerprint
 *        is a match or not.  If NULL, then a hardwired list is
 *        used. Useful for loading fingerprints data from custom
 *        sources.
 *
 * \return 1 (true) if SQLi, 0 (false) if benign
 */
int is_sqli(sfilter * sql_state, const char *s, size_t slen,
            ptr_fingerprints_fn fn);

/**
 * As is_sqli() but for two argument callback function.
 **/
int is_sqli2(sfilter * sql_state, const char *s, size_t slen,
             ptr_fingerprints2_fn fn, void *cbdata);

/**
 * This detects SQLi in a single context, mostly useful for custom
 * logic and debugging.
 *
 * \param sql_state
 * \param s
 * \param slen
 * \param delim must be char of
 *        CHAR_NULL (\0), raw context
 *        CHAR_SINGLE ('), single quote context
 *        CHAR_DOUBLE ("), double quote context
 *        Other values will likely be ignored.
 * \param ptr_fingerprints_fn is a pointer to a function
 *        that determines if a fingerprint is a match or not.
 *
 *
 * \return 1 (true) if SQLi or 0 (false) if not SQLi **in this context**
 *
 */
int is_string_sqli(sfilter * sql_state, const char *s, size_t slen,
                   const char delim,
                   ptr_fingerprints_fn fn);

/**
 * As is_string_sqli2() but for two argument callback function.
 **/
int is_string_sqli2(sfilter * sql_state, const char *s, size_t slen,
                    const char delim,
                    ptr_fingerprints2_fn fn, void *cbdata);

/**
 * DEPRECATED -- HERE FOR BACKWARDS COMPATIBILITY
 * This is the default lookup of a fingerprint
 *
 * /param key c-string of fingerprint
 * /return 1 (TRUE) if a match, 0 (FALSE) if not
 *
 */
int is_sqli_pattern(const char *key);

#ifdef __cplusplus
}
#endif

#endif /* _SQLPARSE_H */
