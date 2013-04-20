/* -*- mode: c++; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */

/*
 * <pre>
 * modp_xml xml decoders
 * http://code.google.com/p/stringencoders/
 *
 * Copyright &copy; 2012  Nick Galbreath -- nickg [at] client9 [dot] com
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *   Redistributions of source code must retain the above copyright
 *   notice, this list of conditions and the following disclaimer.
 *
 *   Redistributions in binary form must reproduce the above copyright
 *   notice, this list of conditions and the following disclaimer in the
 *   documentation and/or other materials provided with the distribution.
 *
 *   Neither the name of the modp.com nor the names of its
 *   contributors may be used to endorse or promote products derived from
 *   this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * This is the standard "new" BSD license:
 * http://www.opensource.org/licenses/bsd-license.php
 * </PRE>
 */
#include "modp_xml.h"

static const uint32_t gsHexDecodeMap[256] = {
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
  0,   1,   2,   3,   4,   5,   6,   7,   8,   9, 256, 256,
256, 256, 256, 256, 256,  10,  11,  12,  13,  14,  15, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256,  10,  11,  12,  13,  14,  15, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
256, 256, 256, 256
};

size_t modp_xml_unicode_char_to_utf8(char* dest, uint32_t uval)
{
    if (uval <= 0x7F) {
        dest[0] = (char) uval;
        return 1;
    }
    if (uval <= 0x7FF) {
        dest[0] = (char)((uval >> 6) + 0xC0);
        dest[1] = (char)((uval & 63) + 0x80);
        return 2;
    }
    if (uval <= 0xFFFF) {
        dest[0] = (char)((uval >> 12) + 224);
        dest[1] = (char)(((uval >>  6) & 63) + 128);
        dest[2] = (char)((uval & 63) + 128);
        return 3;
    }
    if (uval <= 0x1FFFFF) {
        dest[0] = (char)((uval >> 18) + 240);
        dest[1] = (char)(((uval >> 12) & 63) + 128);
        dest[2] = (char)(((uval >> 6) & 63) + 128);
        dest[3] = (char)((uval & 63) + 128);
        return 4;
    }
    return 0;
}


/**
 * Returns 0 if unicode code point is invalid for HTML (undefined or a
 * non-whitespace control char).
 *
 * Exposed for testing
 *
 * http://www.whatwg.org/specs/web-apps/current-work/multipage/syntax.html#character-references
 * Retrieved 20120811:

 * The numeric character reference forms described above are allowed
 * to reference any Unicode code point other than U+0000, U+000D,
 * permanently undefined Unicode characters (noncharacters), and
 * control characters other than space characters.
 */
uint32_t modp_xml_validate_unicode(uint32_t val)
{
    static const uint32_t ranges[] = {
        0x0000, 0x0008, /* control characters */
        0x000B, 0x000B, /* Vertical Tab is forbidden, ?? */
        0x000E, 0x001F, /* control characters */
        0x0080, 0x009F, /* control characters */
        0x0750, 0x077D, /* the rest are undefined */
        0x07C0, 0x08FF,
        0x1380, 0x139F,
        0x18B0, 0x18FF,
        0x1980, 0x19DF,
        0x1A00, 0x1CFF,
        0x1D80, 0x1DFF,
        0x2C00, 0x2E7F,
        0x2FE0, 0x2FEF,
        0x31C0, 0x31EF,
        0x9FB0, 0x9FFF,
        0xA4D0, 0xABFF,
        0xD7B0, 0xD7FF,
        0xFE10, 0xFE1F,
        0x10140, 0x102FF,
        0x104B0, 0x107FF,
        0x1D200, 0x1D2FF,
        0x1D360, 0x1D3FF,
        0x1D800, 0x1FFFF,
        0x2A6E0, 0x2F7FF,
        0x2FAB0, 0xDFFFF,
        0xE0080, 0xE00FF,
        0xE01F0, 0xEFFFF,
        0xFFFFE, 0xFFFFF
    };

    static const int imax = sizeof(ranges)/sizeof(uint32_t);

    int i;
    for (i = 0; i < imax; i += 2) {
        if (val >= ranges[i]) {
            if (val <= ranges[i+1]) {
                return 0;
            }
        } else {
            return val;
        }
    }
    return 0;
}

/**
 * Exposed for testing
 */

uint32_t modp_xml_parse_dec_entity(const char* s, size_t len)
{
    uint32_t val = 0;
    size_t i;
    for (i = 0; i < len; ++i) {
        uint32_t d = gsHexDecodeMap[(unsigned int)s[i]];
        if (d > 9) {
            return 0;
        }
        val = (val * 10) + d;
        if (val > 0x1000FF) {
            return 0;
        }
    }
    return modp_xml_validate_unicode(val);
}

/**
 * parses
 * Exposed for testing
 */
uint32_t modp_xml_parse_hex_entity(const char* s, size_t len)
{
    uint32_t val = 0;
    size_t i;
    for (i = 0; i < len; ++i) {
        uint32_t d = gsHexDecodeMap[(unsigned int)s[i]];
        if (d == 256) {
            return 0;
        }
        val = (val * 16) + d;
        if (val > 0x1000FF) {
            return 0;
        }
    }
    return modp_xml_validate_unicode(val);
}

size_t modp_xml_decode(char* dest, const char* s, size_t len)
{
    const uint8_t* src = (const uint8_t*) s;
    const char* deststart = dest;
    const uint8_t* srcend = (const uint8_t*)(src + len);
    uint32_t unichar;

    while (src < srcend) {
        if (*src != '&') {
            *dest++ = (char) *src++;
            continue;
        }

        const uint8_t* pos = (const uint8_t*) memchr(src+1, ';',
                                   (size_t)(srcend - src - 1));
        if (pos == NULL) {
            // if not found, just copy
            *dest++ = (char) *src++;
            continue;
        }
        size_t elen = (size_t)(pos - src);
        if (*(src+1) == '#') {
            if (*(src+2) == 'x' || *(src+2) == 'X') {
                unichar = modp_xml_parse_hex_entity((const char*)(src + 3), elen - 3);
            } else {
                //
                unichar = modp_xml_parse_dec_entity((const char*)(src + 2), elen - 2);
            }
            if (unichar == 0) {
                *dest++ = (char) *src++;
            } else {
                dest += modp_xml_unicode_char_to_utf8(dest, unichar);
                src = pos + 1;
            }
        } else if (elen == 5 && src[1] == 'q' && src[2] == 'u' &&
                   src[3] == 'o' && src[4] == 't') {
            *dest++ = '"';
            src = pos + 1;
        } else if (elen == 5 && src[1] == 'a' && src[2] == 'p' &&
                   src[3] == 'o' && src[4] == 's') {
            *dest++ = '\'';
            src = pos + 1;
        } else if (elen == 4 && src[1] == 'a' && src[2] == 'm' &&
                   src[3] == 'p') {
            *dest++ = '&';
            src = pos + 1;
        } else if (elen == 3 && src[1] == 'l' && src[2] == 't') {
            *dest++ = '<';
            src = pos +1 ;
        } else if (elen == 3 && src[1] == 'g' && src[2] == 't') {
            *dest++ = '>';
            src = pos +1 ;
        } else {
            // if not found, just copy
            *dest++ = (char) *src++;
        }
    }

    *dest = '\0';
    return (size_t)(dest - deststart); // compute "strlen" of dest.
}

size_t modp_xml_encode(char* dest, const char* src, size_t len)
{
    size_t count = 0;
    const char* srcend = src + len;
    char ch;
    while (src < srcend) {
        ch = *src++;
        switch (ch) {
        case '&':
            *dest++ = '&';
            *dest++ = 'a';
            *dest++ = 'm';
            *dest++ = 'p';
            *dest++ = ';';
            count += 5; /* &amp; */
            break;
        case '<':
            *dest++ = '&';
            *dest++ = 'l';
            *dest++ = 't';
            *dest++ = ';';
            count += 4; /* &lt; */
            break;
        case '>':
            *dest++ = '&';
            *dest++ = 'g';
            *dest++ = 't';
            *dest++ = ';';
            count += 4; /* &gt; */
            break;
        case '\'':
            *dest++ = '&';
            *dest++ = 'q';
            *dest++ = 'u';
            *dest++ = 'o';
            *dest++ = 't';
            *dest++ = ';';
            count += 6; /* &quot; */
            break;
        case '\"':
            *dest++ = '&';
            *dest++ = 'a';
            *dest++ = 'p';
            *dest++ = 'o';
            *dest++ = 's';
            *dest++ = ';';
            count += 6; /* &apos; */
            break;
        default:
            *dest++ = ch;
            count += 1;
        }
    }
    *dest = '\0';
    return count;
}

size_t modp_xml_min_encode_strlen(const char* src, const size_t len)
{
    size_t count = 0;
    const char* srcend = src + len;
    while (src < srcend) {
        switch (*src++) {
        case '&':
            count += 5; /* &amp; */
            break;
        case '<':
            count += 4; /* &lt; */
            break;
        case '>':
            count += 4; /* &gt; */
            break;
        case '\'':
            count += 6; /* &quot; */
            break;
        case '\"':
            count += 6; /* &apos; */
            break;
        default:
            count += 1;
        }
    }
    return count;
}
