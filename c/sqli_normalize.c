/**
 * Copyright 2012, Nick Galbreath
 * nickg@client9.com
 * BSD License -- see COPYING.txt for details
 *
 * (setq-default indent-tabs-mode nil)
 * (setq c-default-style "k&r"
 *     c-basic-offset 4)
 *  indent -kr -nut
 */


/**
 * /file pre-preprocessing step used on query string data
 *
 * Split out separately since many clients of libinjection might have their own
 * functions that do this.  Also this eliminates dependencies.
 *
 */

#include "sqli_normalize.h"

#include "modp_burl.h"
#include "modp_ascii.h"
#include "modp_xml.h"

size_t sqli_qs_normalize(char *s, size_t slen)
{
    size_t newlen;

    // turn '+' into ' '
    slen = modp_burl_decode(s, s, slen);
    while (1) {
        // plain decode
        newlen = modp_burl_decode_raw(s, s, slen);
        if (slen == newlen) {
            // if no changes in size, we are done
            break;
        }
        slen = newlen;
    }
    // due to bad cut-n-paste we see HTML entities in
    // query strings and post vars.  Decode so we aren't
    // trying to make "&quot;" as "& quot ;" in sql
    slen = modp_xml_decode(s, s, slen);

    // upcase
    modp_toupper(s, slen);

    return slen;
}
