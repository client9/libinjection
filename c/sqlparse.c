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

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <assert.h>

// order is important here
#include "sqlparse_private.h"
#include "sqlparse_data.h"

bool streq(const char *a, const char *b)
{
    return strcmp(a, b) == 0;
}

void st_clear(stoken_t * st)
{
    st->type = CHAR_NULL;
    st->val[0] = CHAR_NULL;
}

bool st_is_empty(const stoken_t * st)
{
    return st->type == CHAR_NULL;
}

void st_assign_char(stoken_t * st, const char stype, const char value)
{
    st->type = stype;
    st->val[0] = value;
    st->val[1] = CHAR_NULL;
}

void st_assign(stoken_t * st, const char stype, const char *value,
               size_t len)
{
    size_t last = len < (ST_MAX_SIZE - 1) ? len : (ST_MAX_SIZE - 1);
    st->type = stype;
    strncpy(st->val, value, last);
    st->val[last] = CHAR_NULL;
}

void st_assign_cstr(stoken_t * st, const char stype, const char *value)
{
    st->type = stype;
    strncpy(st->val, value, ST_MAX_SIZE - 1);
    st->val[ST_MAX_SIZE - 1] = CHAR_NULL;
}

bool st_equals_cstr(const stoken_t * st, const char stype,
                    const char *value)
{
    return st->type == stype && !strcmp(value, st->val);
}

void st_copy(stoken_t * dest, const stoken_t * src)
{
    memcpy(dest, src, sizeof(stoken_t));
}

const char *bsearch_cstr(const char *key, const char *base[], size_t nmemb)
{

    int pos;
    int left = 0;
    int right = (int) nmemb - 1;
    int cmp = 0;

    while (left <= right) {
        pos = (left + right) / 2;
        cmp = strcmp(base[pos], key);
        if (cmp == 0) {
            return base[pos];
        } else if (cmp < 0) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }
    return NULL;
}

char bsearch_keyword_type(const char *key, const keyword_t * keywords,
                          size_t numb)
{
    int left = 0;
    int right = (int) numb - 1;

    while (left <= right) {
        int pos = (left + right) / 2;
        int cmp = strcmp(keywords[pos].word, key);
        if (cmp == 0) {
            return keywords[pos].type;
        } else if (cmp < 0) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }

    return CHAR_NULL;
}

bool is_operator2(const char *key)
{
    return bsearch_cstr(key, operators2, operators2_sz) != NULL;
}

bool st_is_multiword_start(const stoken_t * st)
{
    return bsearch_cstr(st->val,
                        multikeywords_start,
                        multikeywords_start_sz) != NULL;
}

bool st_is_english_op(const stoken_t * st)
{
    return (st->type == 'o' && !(strcmp(st->val, "AND") &&
                                 strcmp(st->val, "&") &&
                                 strcmp(st->val, "NOT") &&
                                 strcmp(st->val, "UNION") &&
                                 strcmp(st->val, "CASE") &&
                                 strcmp(st->val, "LIKE") &&
                                 strcmp(st->val, "IS") &&
                                 strcmp(st->val, "MOD"))
        );
}

bool st_is_unary_op(const stoken_t * st)
{
    return (st->type == 'o' && !(strcmp(st->val, "+") &&
                                 strcmp(st->val, "-") &&
                                 strcmp(st->val, "!") &&
                                 strcmp(st->val, "!!") &&
                                 strcmp(st->val, "NOT") &&
                                 strcmp(st->val, "~")));
}

bool st_is_arith_op(const stoken_t * st)
{
    return (st->type == 'o' && !(strcmp(st->val, "-") &&
                                 strcmp(st->val, "+") &&
                                 strcmp(st->val, "~") &&
                                 strcmp(st->val, "!") &&
                                 strcmp(st->val, "/") &&
                                 strcmp(st->val, "%") &&
                                 strcmp(st->val, "*") &&
                                 strcmp(st->val, "|") &&
                                 strcmp(st->val, "&") &&
                                 strcmp(st->val, "MOD") &&
                                 strcmp(st->val, "DIV")));
}

size_t parse_white(sfilter * sf)
{
    return sf->pos + 1;
}

size_t parse_operator1(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    size_t pos = sf->pos;

    st_assign_char(current, 'o', cs[pos]);
    return pos + 1;
}

size_t parse_other(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    size_t pos = sf->pos;

    st_assign_char(current, '?', cs[pos]);
    return pos + 1;
}

size_t parse_char(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    size_t pos = sf->pos;

    st_assign_char(current, cs[pos], cs[pos]);
    return pos + 1;
}

size_t parse_eol_comment(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;

    const char *endpos =
        (const char *) memchr((const void *) (cs + pos), '\n', slen - pos);
    if (endpos == NULL) {
        st_assign_cstr(current, 'c', cs + pos);
        return slen;
    } else {
        st_assign(current, 'c', cs + pos, endpos - cs - pos);
        return (endpos - cs) + 1;
    }
}

size_t parse_dash(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;


    size_t pos1 = pos + 1;
    if (pos1 < slen && cs[pos1] == '-') {
        return parse_eol_comment(sf);
    } else {
        st_assign_char(current, 'o', '-');
        return pos1;
    }
}

size_t is_mysql_comment(const char *cs, const size_t len, size_t pos)
{
    size_t i;

    if (pos + 2 >= len) {
        return 0;
    }
    if (cs[pos + 2] != '!') {
        return 0;
    }
    // this is a mysql comment
    // got "/*!"
    if (pos + 3 >= len) {
        return 3;
    }

    if (!isdigit(cs[pos + 3])) {
        return 3;
    }
    // handle odd case of /*!0SELECT
    if (!isdigit(cs[pos + 4])) {
        return 4;
    }

    if (pos + 7 >= len) {
        return 4;
    }

    for (i = pos + 5; i <= pos + 7; ++i) {
        if (!isdigit(cs[i])) {
            return 3;
        }
    }
    return 8;
}

size_t parse_slash(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;

    size_t pos1 = pos + 1;
    if (pos1 == slen || cs[pos1] != '*') {
        return parse_operator1(sf);
    }
    size_t inc = is_mysql_comment(cs, slen, pos);

    if (inc == 0) {
        const char *ptr = strstr(cs + pos, "*/");
        if (ptr == NULL) {
            // unterminated comment
            st_assign_cstr(current, 'c', cs + pos);
            return slen;
        } else {
            st_assign(current, 'c', cs + pos, (ptr + 2) - (cs + pos));
            return (ptr - cs) + 2;
        }
    } else {
        // MySQL Comment
        sf->in_comment = true;
        st_clear(current);
        return pos + inc;
    }
}

size_t parse_backslash(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;

    if (pos + 1 < slen && cs[pos + 1] == 'N') {
        st_assign_cstr(current, 'k', "NULL");
        return pos + 2;
    } else {
        return parse_other(sf);
    }
}

size_t parse_operator2(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;

    if (pos + 1 >= slen) {
        return parse_operator1(sf);
    }
    char op2[3] = { cs[pos], cs[pos + 1], CHAR_NULL };

    // Special Hack for MYSQL style comments
    // instead of turning:
    // /*! FOO */  into FOO by rewriting the string, we
    // turn it into FOO */ and ignore the ending comment
    if (sf->in_comment && op2[0] == '*' && op2[1] == '/') {
        sf->in_comment = false;
        st_clear(current);
        return pos + 2;
    } else if (pos + 2 < slen && op2[0] == '<' && op2[1] == '='
               && cs[pos + 2] == '>') {
        // special 3-char operator

        st_assign_cstr(current, 'o', "<=>");
        return pos + 3;
    } else if (is_operator2(op2)) {
        if (streq(op2, "&&") || streq(op2, "||")) {
            st_assign_cstr(current, '&', op2);
        } else {
            // normal 2 char operator
            st_assign_cstr(current, 'o', op2);
        }
        return pos + 2;
    } else {
        // must be a single char operator
        return parse_operator1(sf);
    }
}

size_t parse_string_core(const char *cs, const size_t len, size_t pos,
                         stoken_t * st, char delim, size_t offset)
{
    // offset is to skip the perhaps first quote char
    const char *qpos =
        (const char *) memchr((const void *) (cs + pos + offset), delim,
                              len - pos - offset);
    while (true) {
        if (qpos == NULL) {
            st_assign_cstr(st, 's', cs + pos);
            return len;
        } else if (*(qpos - 1) != '\\') {
            st_assign(st, 's', cs + pos, qpos - (cs + pos) + 1);
            return qpos - cs + 1;
        } else {
            qpos =
                (const char *) memchr((const void *) (qpos + 1), delim,
                                      (cs + len) - (qpos + 1));
        }
    }
}

/**
 * Used when first char is a ' or "
 */
size_t parse_string(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;

    // assert cs[pos] == single or double quote
    return parse_string_core(cs, slen, pos, current, cs[pos], 1);
}

size_t parse_word(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    //const size_t slen = sf->slen;
    size_t pos = sf->pos;

    // BUG BUG BUG.. does not take into account line length
    size_t slen =
        strspn(cs + pos, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.$");

    st_assign(current, 'n', cs + pos, slen);
    if (slen < ST_MAX_SIZE) {
        char ch =
            bsearch_keyword_type(current->val, sql_keywords,
                                 sql_keywords_sz);
        if (ch == CHAR_NULL) {
            ch = 'n';
        }
        current->type = ch;
    }
    return pos + slen;
}

size_t parse_var(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;

    size_t pos1 = pos + 1;

    // move past optional other '@'
    if (pos1 < slen && cs[pos1] == '@') {
        pos1 += 1;
    }

    size_t xlen =
        strspn(cs + pos1, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.$");
    if (xlen == 0) {
        st_assign(current, 'v', cs + pos, (pos1 - pos));
        return pos1;
    } else {
        st_assign(current, 'v', cs + pos, xlen + (pos1 - pos));
        return pos1 + xlen;
    }
}

size_t parse_number(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *cs = sf->s;
    const size_t slen = sf->slen;
    size_t pos = sf->pos;

    if (pos + 1 < slen && cs[pos] == '0' && cs[pos + 1] == 'X') {
        // TBD compare if isxdigit
        size_t xlen = strspn(cs + pos + 2, "0123456789ABCDEF");
        if (xlen == 0) {
            st_assign_cstr(current, 'n', "0X");
            return pos + 2;
        } else {
            st_assign(current, '1', cs + pos, 2 + xlen);
            return pos + 2 + xlen;
        }
    }
    size_t start = pos;

    while (isdigit(cs[pos])) {
        pos += 1;
    }
    if (cs[pos] == '.') {
        pos += 1;
        while (pos < slen && isdigit(cs[pos])) {
            pos += 1;
        }
        if (pos - start == 1) {
            st_assign_char(current, 'n', '.');
            return pos;
        }
    }

    if (cs[pos] == 'E') {
        pos += 1;
        if (pos < slen && (cs[pos] == '+' || cs[pos] == '-')) {
            pos += 1;
        }
        while (isdigit(cs[pos])) {
            pos += 1;
        }
    } else if (isalpha(cs[pos])) {
        // oh no, we have something like '6FOO'
        // which is not a number, grab as many alphanum
        // as possible
        pos += 1;
        while (pos < slen && isalnum(cs[pos])) {
            pos += 1;
        }
        st_assign(current, 'n', cs + start, pos - start);
        return pos;
    }

    st_assign(current, '1', cs + start, pos - start);
    return pos;
}

bool parse_token(sfilter * sf)
{
    stoken_t *current = &sf->syntax_current;
    const char *s = sf->s;
    const size_t slen = sf->slen;
    size_t *pos = &sf->pos;

    st_clear(current);

    if (*pos == 0 && sf->delim != CHAR_NULL) {
        *pos = parse_string_core(s, slen, 0, current, sf->delim, 0);
        return true;
    }

    while (*pos < slen) {
        const int ch = (int) (s[*pos]);
        if (ch < 0 || ch > 127) {
            *pos += 1;
            continue;
        }
        pt2Function fnptr = char_parse_map[ch];
        *pos = (*fnptr) (sf);
        if (current->type != CHAR_NULL) {
            //printf("POS = %d, %s \n", *pos, st->val);
            return true;
        }
    }
    return false;
}

void sfilter_reset(sfilter * sf, const char *s, size_t len)
{
    memset(sf, 0, sizeof(sfilter));
    sf->s = s;
    sf->slen = len;
}

bool syntax_merge_words(stoken_t * a, stoken_t * b)
{
    if (!
        (a->type == 'k' || a->type == 'n' || a->type == 'o'
         || a->type == 'U')) {
        return false;
    }

    size_t sz1 = strlen(a->val);
    size_t sz2 = strlen(b->val);
    size_t sz3 = sz1 + sz2 + 1;
    if (sz3 >= ST_MAX_SIZE) {
        return false;
    }
    // oddly annoying  last.val + ' ' + current.val
    char tmp[ST_MAX_SIZE];
    memcpy(tmp, a->val, sz1);
    tmp[sz1] = ' ';
    memcpy(tmp + sz1 + 1, b->val, sz2);
    tmp[sz3] = CHAR_NULL;

    //printf("\nTMP = %s\n", tmp);
    char ch = bsearch_keyword_type(tmp, multikeywords, multikeywords_sz);
    if (ch != CHAR_NULL) {
        // -1, don't copy the null byte
        st_assign(a, ch, tmp, sz3);
        return true;
    } else {
        return false;
    }
}

bool sqli_tokenize(sfilter * sf, stoken_t * sout)
{
    stoken_t *last = &sf->syntax_last;
    stoken_t *current = &sf->syntax_current;

    while (parse_token(sf)) {
        char ttype = current->type;
        if (ttype == 'c') {
            st_copy(&sf->syntax_comment, current);
            continue;
        }
        st_clear(&sf->syntax_comment);

        //
        // If we don't have a saved token
        //
        if (last->type == CHAR_NULL) {
            switch (ttype) {

                // items that have special needs
            case 's':
                st_copy(last, current);
                continue;
            case 'n':
            case 'k':
            case 'U':
            case '&':
            case 'o':
                if (st_is_multiword_start(current)) {
                    st_copy(last, current);
                    continue;
                } else if (current->type == 'o' || current->type == '&') {
                    //} else if (st_is_unary_op(current)) {
                    st_copy(last, current);
                    continue;
                } else {
                    // copy to out
                    st_copy(sout, current);
                    return true;
                }
            default:
                // copy to out
                st_copy(sout, current);
                return true;
            }
        }
        //
        // We have a saved token
        //

        switch (ttype) {
        case 's':
            if (last->type == 's') {
                // "FOO" "BAR" == "FOO" (skip second string)
                continue;
            } else {
                st_copy(sout, last);
                st_copy(last, current);
                return true;
            }
            break;

        case 'o':
            // first case to handle "IS" + "NOT"
            if (syntax_merge_words(last, current)) {
                continue;
            } else if (st_is_unary_op(current)
                       && (last->type == 'o' || last->type == '&'
                           || last->type == 'U')) {
                // if an operator is followed by a unary operator, skip it.
                // 1, + ==> "+" is not unary, it's arithmetic
                // AND, + ==> "+" is unary
                continue;
            } else {
                // no match
                st_copy(sout, last);
                st_copy(last, current);
                return true;
            }
            break;

        case 'n':
        case 'k':
            if (syntax_merge_words(last, current)) {
                continue;
            } else {
                // total no match
                st_copy(sout, last);
                st_copy(last, current);
                return true;
            }
            break;

        default:
            // fix up for ambigous "IN"
            // handle case where IN is typically a function
            // but used in compound "IN BOOLEAN MODE" jive
            if (last->type == 'n' && !strcmp(last->val, "IN")) {
                st_copy(last, current);
                st_assign_cstr(sout, 'f', "IN");
                return true;
            } else {
                // no match at all
                st_copy(sout, last);
                st_copy(last, current);
                return true;
            }
            break;
        }
    }

    // final cleanup
    if (last->type) {
        st_copy(sout, last);
        st_clear(last);
        return true;
    } else if (sf->syntax_comment.type) {
        st_copy(sout, &sf->syntax_comment);
        st_clear(&sf->syntax_comment);
        return true;
    } else {
        return false;
    }
}

bool filter_fold(sfilter * sf, stoken_t * sout)
{
    stoken_t *last = &sf->fold_last;
    stoken_t *current = &sf->fold_current;

    //printf("state = %d\n", sf->fold_state);
    if (sf->fold_state == 4 && !st_is_empty(last)) {
        //printf("LINE = %d\n", __LINE__);
        st_copy(sout, last);
        //printf("%d emit = %c, %s\n", __LINE__, sout->type, sout->val);
        sf->fold_state = 2;
        st_clear(last);
        return true;
    }

    while (sqli_tokenize(sf, current)) {
        //printf("state = %d\n", sf->fold_state);
        //printf("current = %c, %s\n", current->type, current->val);
        if (sf->fold_state == 0) {
            if (current->type == '(') {
                continue;
            }
            if (st_is_unary_op(current)) {
                continue;
            }
            sf->fold_state = 1;
        }

        if (st_is_empty(last)) {
            //printf("LINE = %d\n", __LINE__);
            if (current->type == '1') {
                //printf("LINE = %d\n", __LINE__);
                sf->fold_state = 2;
                st_copy(last, current);
            }
            //printf("LINE = %d\n", __LINE__);
            st_copy(sout, current);
            //printf("emit = %c, %s\n", sout->type, sout->val);
            return true;
        } else if (last->type == '1' && st_is_arith_op(current)) {
            //printf("LINE = %d\n", __LINE__);
            st_copy(last, current);
            //sf->fold_state = 1;
        } else if (last->type == 'o' && current->type == '1') {
            //printf("LINE = %d\n", __LINE__);
            //continue;
            st_copy(last, current);
        } else {
            //printf("LINE = %d\n", __LINE__);
            if (sf->fold_state == 2) {
                if (last->type != '1') {
                    st_copy(sout, last);
                    st_copy(last, current);
                    // printf("%d emit = %c, %s\n", __LINE__, sout->type, sout->val);
                    sf->fold_state = 4;
                } else {
                    st_copy(sout, current);
                    st_clear(last);
                }
                return true;
            } else {
                //printf("LINE = %d\n", __LINE__);
                if (last->type == 'o') {
                    //printf("STATE = %d, LINE = %d\n", sf->fold_state, __LINE__);
                    st_copy(sout, last);
                    st_copy(last, current);
                    sf->fold_state = 4;
                } else {
                    //printf("LINE = %d\n", __LINE__);
                    sf->fold_state = 2;
                    st_copy(sout, current);
                    st_clear(last);
                }
                //printf("emit = %c, %s\n", sout->type, sout->val);
                return true;
            }
        }
    }

    if (!st_is_empty(last)) {
        if (st_is_arith_op(last)) {
            //printf("\nstate = %d, emit = %c, %s\n", sf->fold_state, last->type, last->val);
            st_copy(sout, last);
            st_clear(last);
            return true;
        } else {
            st_clear(last);
        }
    }

    return false;
}

bool is_string_sqli(sfilter * sql_state, const char *s, size_t slen,
                    const char delim, ptr_fingerprints_fn fn)
{
    sfilter_reset(sql_state, s, slen);
    sql_state->delim = delim;

    bool all_done = false;
    int tlen = 0;
    while (tlen < MAX_TOKENS) {
        all_done = filter_fold(sql_state, &(sql_state->tokenvec[tlen]));
        if (!all_done) {
            break;
        }

        sql_state->pat[tlen] = sql_state->tokenvec[tlen].type;

        //printf("i = %d, char = %c, %s\n", tlen, sql_state->pat[tlen],
        //       sql_state->tokenvec[tlen].val);
        tlen += 1;
    }
    sql_state->pat[tlen] = CHAR_NULL;

    //assert(strlen(sql_state->pat) <= 5);

    //printf("PAT = %s\n", sql_state->pat);

    // check to make sure we don't have a dangling
    // function without a "(" (then it's not a function)
    // (and then not a SQLi).  This is the only reason
    // we need the 6th token.  It might be possible to
    // skip the parsing if token 5 is NOT a function type

    if (tlen == MAX_TOKENS && !all_done
        && sql_state->pat[MAX_TOKENS - 1] == 'f') {

        stoken_t tmp;
        all_done = filter_fold(sql_state, &tmp);
        if (!all_done && tmp.type != '(') {
            sql_state->reason = __LINE__;
            return false;
        }
    }

    bool patmatch = fn(sql_state->pat);
    //bool patmatch = false;
    if (!patmatch) {
        sql_state->reason = __LINE__;
        return false;
    }
    switch (tlen) {

    case 3:{
            if (streq(sql_state->pat, "sos") &&
                (st_is_arith_op(&sql_state->tokenvec[1]) ||
                 st_is_english_op(&sql_state->tokenvec[1]) ||
                 sql_state->delim == CHAR_NULL)) {
                sql_state->reason = __LINE__;
                return false;
            } else {
                return true;
            }
        }
        break;
    case 5:{

            if (sql_state->pat[1] == 'o' && sql_state->pat[3] == 'o') {

                if (sql_state->pat[2] == 'v') {
                    return true;
                } else if (streq(sql_state->pat, "sono1") &&
                           st_equals_cstr(&sql_state->tokenvec[1], 'o',
                                          "&")
                           && st_equals_cstr(&sql_state->tokenvec[3], 'o',
                                             "=")) {
                    // query string fragment ...foo"&page=2
                    sql_state->reason = __LINE__;
                    return false;
                } else if (sql_state->delim == CHAR_NULL &&
                           streq(sql_state->pat, "sosos")) {
                    // "foo" and "bar" and "dingbat"
                    //   likely search term
                    sql_state->reason = __LINE__;
                    return false;
                } else if (!st_is_arith_op(&sql_state->tokenvec[3]) &&
                           strcmp(sql_state->tokenvec[1].val,
                                  sql_state->tokenvec[3].val)) {
                    return true;
                } else if (streq(sql_state->tokenvec[1].val,
                                 sql_state->tokenvec[3].val)) {
                    sql_state->reason = __LINE__;
                    return false;
                } else {
                    sql_state->reason = __LINE__;
                    //printf("False: %s not slqi\n", sql_state->pat);
                    return false;
                }
            }
        }
        break;

    }                           /* end switch */

    //printf("i = %d, PAT = %s\n", i, sql_state->pat);
    return true;
}

bool is_sqli(sfilter * sql_state, const char *s, size_t slen,
             ptr_fingerprints_fn fn)
{

    if (is_string_sqli(sql_state, s, slen, CHAR_NULL, fn)) {
        return true;
    }

    if (memchr(s, CHAR_SINGLE, slen)
        && is_string_sqli(sql_state, s, slen, CHAR_SINGLE, fn)) {
        return true;
    }

    if (memchr(s, CHAR_DOUBLE, slen)
        && is_string_sqli(sql_state, s, slen, CHAR_DOUBLE, fn)) {
        return true;
    }

    return false;
}

/*
 not used yet

// [('o', 228), ('k', 220), ('1', 217), (')', 157), ('(', 156), ('s', 154), ('n', 77), ('f', 73), (';', 59), (',', 35), ('v', 17), ('c', 15),
int char2int(char c)
{
    const char *map = "ok1()snf;,";
    const char *pos = strchr(map, c);
    if (pos == NULL) {
        return 15;
    } else {
        return (int) (pos - map) + 1;
    }
}

unsigned long long pat2int(const char *pat)
{
    unsigned long long val = 0;
    while (*pat) {
        val = (val << 4) + char2int(*pat);
        pat += 1;
    }
    return val;
}
*/
