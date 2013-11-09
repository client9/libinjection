#include "libinjection_html5.h"

#include <string.h>
#include <assert.h>

#define DEBUG
#ifdef DEBUG
#include <stdio.h>
#define TRACE() printf("%s:%d\n", __FUNCTION__, __LINE__)
#else
#define TRACE()
#endif


#define CHAR_EOF -1
#define CHAR_NULL 0
#define CHAR_BANG 33
#define CHAR_DOUBLE 34
#define CHAR_SINGLE 39
#define CHAR_DASH 45
#define CHAR_SLASH 47
#define CHAR_LT 60
#define CHAR_EQUALS 61
#define CHAR_GT 62
#define CHAR_QUESTION 63
#define CHAR_TICK 96

/* prototypes */

static int h5_skip_white(h5_state_t* hs);
static int h5_is_white(char c);
static int h5_state_eof(h5_state_t* hs);
static int h5_state_data(h5_state_t* hs);
static int h5_state_tag_open(h5_state_t* hs);
static int h5_state_tag_name(h5_state_t* hs);
static int h5_state_tag_name_close(h5_state_t* hs);
static int h5_state_end_tag_open(h5_state_t* hs);
static int h5_state_self_closing_start_tag(h5_state_t* hs);
static int h5_state_attribute_name(h5_state_t* hs);
static int h5_state_after_attribute_name(h5_state_t* hs);
static int h5_state_before_attribute_name(h5_state_t* hs);
static int h5_state_before_attribute_value(h5_state_t* hs);
static int h5_state_attribute_value_double_quote(h5_state_t* hs);
static int h5_state_attribute_value_single_quote(h5_state_t* hs);
static int h5_state_attribute_value_no_quote(h5_state_t* hs);
static int h5_state_after_attribute_value_quoted_state(h5_state_t* hs);
static int h5_state_comment(h5_state_t* hs);

/* 12.2.4.44 */
static int h5_state_bogus_comment(h5_state_t* hs);

/* 12.2.4.45 */
static int h5_state_markup_declaration_open(h5_state_t* hs);

/**
 * public function
 */
void libinjection_h5_init(h5_state_t* hs, const char* s, size_t len, int flags)
{
    memset(hs, 0, sizeof(h5_state_t));
    hs->s = s;
    hs->len = len;
    hs->state = h5_state_data;
    if (flags == 0) {
        hs->state = h5_state_data;
    } else {
        assert(0);
    }
}

/**
 * public function
 */
int libinjection_h5_next(h5_state_t* hs)
{
    assert(hs->state != NULL);
    return (*hs->state)(hs);
}

/**
 * Everything below here is private
 *
 */

static int h5_is_white(char ch)
{
    return strchr(" \t\n\v\f\r", ch) != NULL;
}

static int h5_skip_white(h5_state_t* hs)
{
    char ch;
    while (hs->pos < hs->len) {
        ch = hs->s[hs->pos];
        if (ch == ' ') {
            hs->pos += 1;
        } else {
            return ch;
        }
    }
    return CHAR_EOF;
}

static int h5_state_eof(h5_state_t* hs)
{
    /* eliminate unused function argument warning */
    (void)hs;
    return 0;
}

static int h5_state_data(h5_state_t* hs)
{
    TRACE();
    assert(hs->len >= hs->pos);
    const char* idx = (const char*) memchr(hs->s + hs->pos, CHAR_LT, hs->len - hs->pos);
    if (idx == NULL) {
        hs->token_start = hs->s + hs->pos;
        hs->token_len = hs->len - hs->pos;
        hs->token_type = DATA_TEXT;
        hs->state = h5_state_eof;
        if (hs->token_len == 0) {
            return 0;
        }
    } else {
        hs->token_start = hs->s + hs->pos;
        hs->token_type = DATA_TEXT;
        hs->token_len = idx - (hs->s + hs->pos);
        hs->pos = (idx - hs->s) + 1;
        hs->state = h5_state_tag_open;
        if (hs->token_len == 0) {
            return h5_state_tag_open(hs);
        }
    }
    return 1;
}

/**
 * 12 2.4.8
 */
static int h5_state_tag_open(h5_state_t* hs)
{
    TRACE();
    char ch = hs->s[hs->pos];
    if (ch == CHAR_BANG) {
        hs->pos += 1;
        return h5_state_markup_declaration_open(hs);
    } else if (ch == CHAR_SLASH) {
        hs->pos += 1;
        hs->is_close = 1;
        return h5_state_end_tag_open(hs);
    } else if (ch == CHAR_QUESTION) {
        hs->pos += 1;
        return h5_state_bogus_comment(hs);
    } else if ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z')) {
        return h5_state_tag_name(hs);
    } else {
        hs->token_start = hs->s + hs->pos;
        hs->token_len = 1;
        hs->token_type = DATA_TEXT;
        hs->state = h5_state_data;
        return 1;
    }
}
/**
 * 12.2.4.9
 */
static int h5_state_end_tag_open(h5_state_t* hs)
{
    TRACE();
    char ch;

    if (hs->pos >= hs->len) {
        return 0;
    }
    ch = hs->s[hs->pos];
    if (ch == CHAR_GT) {
        return h5_state_data(hs);
    } else if ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z')) {
        return h5_state_tag_name(hs);
    }
    return h5_state_data(hs);
}
/*
 *
 */
static int h5_state_tag_name_close(h5_state_t* hs)
{
    TRACE();
    hs->is_close = 0;
    hs->token_start = hs->s + hs->pos;
    hs->token_len = 1;
    hs->token_type = TAG_NAME_CLOSE;
    hs->pos += 1;
    if (hs->pos < hs->len) {
        printf("case 1\n");
        hs->state = h5_state_data;
    } else {
        printf("case 2\n");
        hs->state = h5_state_eof;
    }

    return 1;
}

/**
 * 12.2.4.10
 */
static int h5_state_tag_name(h5_state_t* hs)
{
    TRACE();
    char ch;
    size_t pos = hs->pos;
    while (pos < hs->len) {
        ch = hs->s[pos];
        if (h5_is_white(ch)) {
            hs->token_start = hs->s + hs->pos;
            hs->token_len = pos - hs->pos;
            hs->token_type = TAG_NAME_OPEN;
            hs->pos = pos + 1;
            hs->state = h5_state_before_attribute_name;
            return 1;
        } else if (ch == CHAR_SLASH) {
            hs->token_start = hs->s + hs->pos;
            hs->token_len = pos - hs->pos;
            hs->token_type = TAG_NAME_OPEN;
            hs->pos = pos + 1;
            hs->state = h5_state_self_closing_start_tag;
            return 1;
        } else if (ch == CHAR_GT) {
            hs->token_start = hs->s + hs->pos;
            hs->token_len = pos - hs->pos;
            if (hs->is_close) {
                hs->pos = pos + 1;
                hs->is_close = 0;
                hs->token_type = TAG_CLOSE;
                hs->state = h5_state_data;
            } else {
                hs->pos = pos;
                hs->token_type = TAG_NAME_OPEN;
                hs->state = h5_state_tag_name_close;
            }
            return 1;
        } else {
            pos += 1;
        }
    }

    hs->token_start = hs->s + hs->pos;
    hs->token_len = hs->len - hs->pos;
    hs->token_type = TAG_NAME_OPEN;
    hs->state = h5_state_eof;
    return 1;
}

/**
 * 12.2.4.34
 */
static int h5_state_before_attribute_name(h5_state_t* hs)
{
    TRACE();
    int ch = h5_skip_white(hs);
    switch (ch) {
    case CHAR_EOF: {
        return 0;
    }
    case CHAR_SLASH: {
        hs->pos += 1;
        return h5_state_self_closing_start_tag(hs);
    }
    case CHAR_GT: {
        hs->state = h5_state_data;
        hs->token_start = hs->s + hs->pos;
        hs->token_len = 1;
        hs->token_type = TAG_NAME_CLOSE;
        hs->pos += 1;
        return 1;
    }
    default: {
        return h5_state_attribute_name(hs);
    }
  }
}

static int h5_state_attribute_name(h5_state_t* hs)
{
    TRACE();
    char ch;
    size_t pos = hs->pos;
    while (pos < hs->len) {
        ch = hs->s[pos];
        if (h5_is_white(ch)) {
            hs->token_start = hs->s + hs->pos;
            hs->token_len   = pos - hs->pos;
            hs->token_type  = ATTR_NAME;
            hs->state = h5_state_after_attribute_name;
            hs->pos = pos + 1;
            return 1;
        } else if (ch == CHAR_SLASH) {
            hs->token_start = hs->s + hs->pos;
            hs->token_len   = pos - hs->pos;
            hs->token_type  = ATTR_NAME;
            hs->state = h5_state_self_closing_start_tag;
            hs->pos = pos + 1;
            return 1;
        } else if (ch == CHAR_EQUALS) {
            hs->token_start = hs->s + hs->pos;
            hs->token_len   = pos - hs->pos;
            hs->token_type  = ATTR_NAME;
            hs->state = h5_state_before_attribute_value;
            hs->pos = pos + 1;
            return 1;
        } else if (ch == CHAR_GT) {
            hs->token_start = hs->s + hs->pos;
            hs->token_len   = pos - hs->pos;
            hs->token_type  = ATTR_NAME;
            hs->state = h5_state_tag_name_close;
            hs->pos = pos + 1;
            return 1;
        } else {
            pos += 1;
        }
    }
    /* EOF */
    hs->token_start = hs->s + hs->pos;
    hs->token_len   = hs->len - hs->pos;
    hs->token_type  = ATTR_NAME;
    hs->state = h5_state_eof;
    hs->pos = hs->len;
    return 1;
}

/**
 * 12.2.4.36
 */
static int h5_state_after_attribute_name(h5_state_t* hs)
{
    TRACE();
    size_t pos = hs->pos;
    int c = h5_skip_white(hs);
    switch (c) {
    case CHAR_EOF: {
        return 0;
    }
    case CHAR_SLASH: {
        hs->pos = pos + 1;
        return h5_state_self_closing_start_tag(hs);
    }
    case CHAR_EQUALS: {
        hs->pos = pos + 1;
        return h5_state_before_attribute_value(hs);
    }
    case CHAR_GT: {
        return h5_state_tag_name_close(hs);
    }
    default: {
        return h5_state_attribute_name(hs);
    }
    }
}

/**
 * 12.2.4.37
 */
static int h5_state_before_attribute_value(h5_state_t* hs)
{
    TRACE();
    int c = h5_skip_white(hs);

    if (c == CHAR_EOF) {
        hs->state = h5_state_eof;
        return 0;
    }

    if (c == CHAR_DOUBLE) {
        return h5_state_attribute_value_double_quote(hs);
    } else if (c == CHAR_SINGLE) {
        return h5_state_attribute_value_single_quote(hs);
    } else {
        return h5_state_attribute_value_no_quote(hs);
    }
}


static int h5_state_attribute_value_quote(h5_state_t* hs, char qchar)
{
    TRACE();
    const char* idx;

    /* skip quote */
    hs->pos += 1;
    idx = memchr(hs->s + hs->pos, qchar, hs->len - hs->pos);
    if (idx == NULL) {
        hs->token_start = hs->s + hs->pos;
        hs->token_len = hs->len - hs->pos;
        hs->token_type = ATTR_VALUE;
        hs->state = h5_state_eof;
    } else {
        hs->token_start = hs->s + hs->pos;
        hs->token_len = idx - (hs->s + hs->pos);
        hs->token_type = ATTR_VALUE;
        hs->state = h5_state_after_attribute_value_quoted_state;
        hs->pos += hs->token_len + 1;
    }
    return 1;
}

static
int h5_state_attribute_value_double_quote(h5_state_t* hs)
{
    TRACE();
    return h5_state_attribute_value_quote(hs, CHAR_DOUBLE);
}

static
int h5_state_attribute_value_single_quote(h5_state_t* hs)
{
    TRACE();
    return h5_state_attribute_value_quote(hs, CHAR_SINGLE);
}

static int h5_state_attribute_value_no_quote(h5_state_t* hs)
{
    TRACE();
    char ch;
    size_t pos = hs->pos;
    while (pos < hs->len) {
        ch = hs->s[pos];
        if (h5_is_white(ch)) {
            hs->token_type = ATTR_VALUE;
            hs->token_start = hs->s + hs->pos;
            hs->token_len = pos - hs->pos;
            hs->pos = pos + 1;
            hs->state = h5_state_before_attribute_name;
            return 1;
        } else if (ch == CHAR_GT) {
            hs->token_type = ATTR_VALUE;
            hs->token_start = hs->s + hs->pos;
            hs->token_len = pos - hs->pos;
            hs->pos = pos + 1;
            hs->state = h5_state_tag_name_close;
            return 1;
        }
        pos += 1;
    }
    TRACE();
    /* EOF */
    hs->state = h5_state_eof;
    hs->token_start = hs->s + hs->pos;
    hs->token_len = hs->len - hs->pos;
    hs->token_type = ATTR_VALUE;
    return 1;
}

/**
 * 12.2.4.41
 */
static int h5_state_after_attribute_value_quoted_state(h5_state_t* hs)
{
    TRACE();
    char ch = hs->s[hs->pos];
    if (h5_is_white(ch)) {
        hs->pos += 1;
        return h5_state_before_attribute_name(hs);
    } else if (ch == CHAR_SLASH) {
        hs->pos += 1;
        return h5_state_self_closing_start_tag(hs);
    } else if (ch == CHAR_GT) {
        hs->token_start = hs->s + hs->pos;
        hs->token_len = 1;
        hs->token_type = TAG_NAME_CLOSE;
        hs->pos += 1;
        hs->state = h5_state_data;
        return 1;
    } else {
        return h5_state_before_attribute_name(hs);
    }
}

/**
 * 12.2.4.43
 */
static int h5_state_self_closing_start_tag(h5_state_t* hs)
{
    TRACE();
    char ch;
    if (hs->pos >= hs->len) {
        return 0;
    }
    ch = hs->s[hs->pos];
    if (ch == CHAR_GT) {
        hs->token_start = hs->s + hs->pos;
        hs->token_len = 2;
        hs->token_type = TAG_NAME_SELFCLOSE;
        hs->state = h5_state_data;
        hs->pos += 1;
        return 1;
    } else {
        return h5_state_before_attribute_name(hs);
    }
}

/**
 * 12.2.4.44
 */
static int h5_state_bogus_comment(h5_state_t* hs)
{
    TRACE();
    const char* idx;
    idx = memchr(hs->s + hs->pos, CHAR_GT, hs->len - hs->pos);
    if (idx == NULL) {
        hs->token_len = hs->len - hs->pos;
        hs->state = h5_state_eof;
    } else {
        hs->token_len = idx - (hs->s + hs->pos);
        hs->state = h5_state_data;
    }
    hs->token_start = hs->s + hs->pos;
    hs->token_type = TAG_COMMENT;
    return 1;
}

/**
 * 12.2.4.45
 */
static int h5_state_markup_declaration_open(h5_state_t* hs)
{
    TRACE();
    size_t remaining = hs->len - hs->pos;
    if (remaining >= 7 &&
               hs->s[hs->pos + 0] == 'D' &&
               hs->s[hs->pos + 1] == 'O' &&
               hs->s[hs->pos + 2] == 'C' &&
               hs->s[hs->pos + 3] == 'T' &&
               hs->s[hs->pos + 4] == 'Y' &&
               hs->s[hs->pos + 5] == 'P' &&
               hs->s[hs->pos + 6] == 'E') {
        assert(0);
    } else if (remaining >=2 &&
               hs->s[hs->pos + 0] == '-' &&
               hs->s[hs->pos + 1] == '-') {
        hs->pos += 2;
        return h5_state_comment(hs);
    } else {
        // CDATA
        assert(0);
    }
}

/**
 * 12.2.4.48
 * 12.2.4.49
 * 12.2.4.50
 * 12.2.4.51
 *   state machine spec is confusing since it can only look
 *   at one character at a time but simply it's comments end by:
 *   1) EOF
 *   2) ending in -->
 *   3) ending in -!>
 */
static int h5_state_comment(h5_state_t* hs)
{
    TRACE();
    char ch;
    const char* idx;
    size_t pos = hs->pos;
    while (1) {
        idx = (const char*) memchr(hs->s + pos, CHAR_DASH, hs->len - pos);

        /* did not find anything or has less than 3 chars left */
        if (idx == NULL || idx > hs->s + hs->len - 3) {
            hs->state = h5_state_eof;
            hs->token_start = hs->s + hs->pos;
            hs->token_len = hs->len - hs->pos;
            hs->token_type = TAG_COMMENT;
            return 1;
        }
        ch = *(idx + 1);
        if (ch != CHAR_DASH && ch != CHAR_BANG) {
            pos = idx - hs->s + 1;
            continue;
        }
        ch = *(idx + 2);
        if (ch != CHAR_GT) {
            pos = idx - hs->s + 2;
            continue;
        }

        /* ends in --> or -!> */
        hs->token_start = hs->s + hs->pos;
        hs->token_len = idx - (hs->s + hs->pos);
        hs->pos = idx - hs->s + 3;
        hs->state = h5_state_data;
        hs->token_type = TAG_COMMENT;
        return 1;
    }
}
