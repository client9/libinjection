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
#define CHAR_NULL '\0'
#define CHAR_SINGLE '\''
#define CHAR_DOUBLE '"'
    typedef struct {
    char type;
    char val[ST_MAX_SIZE];
} stoken_t;


stoken_t *st_new();
void st_destroy(stoken_t ** st);
void st_clear(stoken_t * st);
void st_assign_char(stoken_t * st, const char stype, const char value);
void st_set_type(stoken_t * st, const char stype);
void st_assign(stoken_t * st, const char stype, const char *value,
               size_t len);
void st_assign_cstr(stoken_t * st, const char stype, const char *value);
void st_copy(stoken_t * dest, const stoken_t * src);

bool st_equals_cstr(const stoken_t * src, const char stype,
                    const char *value);

bool st_is_empty(const stoken_t * st);
bool st_is_arith_op(const stoken_t * st);
bool st_is_unary_op(const stoken_t * st);
bool st_is_english_op(const stoken_t * st);
bool st_is_logical_op(const stoken_t * st);
bool st_is_multiword_start(const stoken_t * st);

const char *bsearch_cstr(const char *key, const char *base[],
                         size_t nmemb);

typedef struct {
    const char *word;
    char type;
} keyword_t;

char bsearch_keyword_type(const char *key, const keyword_t keywords[],
                          size_t len);

bool is_operator2(const char *key);
bool is_sqli_pattern(const char *key);


size_t parse_none(const char *cs, const size_t len, size_t pos,
                  stoken_t * st);
size_t parse_other(const char *cs, const size_t len, size_t pos,
                   stoken_t * st);
size_t parse_white(const char *cs, const size_t len, size_t pos,
                   stoken_t * st);
size_t parse_operator1(const char *cs, const size_t len, size_t pos,
                       stoken_t * st);
size_t parse_char(const char *cs, const size_t len, size_t pos,
                  stoken_t * st);
size_t parse_eol_comment(const char *cs, const size_t len, size_t pos,
                         stoken_t * st);
size_t parse_dash(const char *cs, const size_t len, size_t pos,
                  stoken_t * st);
size_t is_mysql_comment(const char *cs, const size_t len, size_t pos);
size_t parse_slash(const char *cs, const size_t len, size_t pos,
                   stoken_t * st);
size_t parse_backslash(const char *cs, const size_t len, size_t pos,
                       stoken_t * st);
size_t parse_operator2(const char *cs, const size_t len, size_t pos,
                       stoken_t * st);
size_t parse_string_core(const char *cs, const size_t len, size_t pos,
                         stoken_t * st, char delim, size_t offset);
size_t parse_string(const char *cs, const size_t len, size_t pos,
                    stoken_t * st);
size_t parse_word(const char *cs, const size_t len, size_t pos,
                  stoken_t * st);
size_t parse_var(const char *cs, const size_t len, size_t pos,
                 stoken_t * st);
size_t parse_number(const char *cs, const size_t len, size_t pos,
                    stoken_t * st);

bool parse_token(const char *cs, const size_t len, size_t * pos,
                 stoken_t * st, char delim);


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

/**
 * Looks at syntax_last and syntax_current to see
 * if they can be merged into a multi-keyword
 */
bool syntax_merge_words(stoken_t * a, stoken_t * b);


/**
 * Takes a raw stream of SQL tokens and does the following:
 * * Merge mutliple strings into one "foo", "bar" --> "foo bar"
 * * Remove comments except last one 1, +, -- foo, 1 ->> 1,+,1
 * * Merge multi-word keywords and operators into one
 *   e.g. "UNION", "ALL" --> "UNION ALL"
 */

bool filter_syntax(sfilter * sf, stoken_t * sout);

bool filter_fold(sfilter * sf, stoken_t * sout);

bool is_string_sqli(sfilter * sql_state, const char *s, size_t slen,
                    const char delim);
bool is_sqli(sfilter * sql_state, const char *s, size_t slen);

unsigned long long pat2int(const char *pat);

CPP_END
#endif
