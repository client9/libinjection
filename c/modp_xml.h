/* -*- mode: c++; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */

/**
 * \file
 * <PRE>
 * High Performance XML Decoder (for now)
 *
 * Copyright &copy; 2012  Nick Galbreath -- nickg [at] client9 [dot] com
 * All rights reserved.
 *
 * http://code.google.com/p/stringencoders/
 *
 * Released under bsd license.  See bfast64.c for details.
 * </PRE>
 */

#ifndef COM_MODP_STRINGENCODERS_XML
#define COM_MODP_STRINGENCODERS_XML

#include "modp_stdint.h"

#ifdef __cplusplus
#define BEGIN_C extern "C" {
#define END_C }
#else
#define BEGIN_C
#define END_C
#endif

BEGIN_C

/**
 * Validates a unicode code point is valid for HTML (undefined or non-white-space control char)
 * http://www.whatwg.org/specs/web-apps/current-work/multipage/syntax.html#character-references
 * Returns 0 if invalid
 */
uint32_t modp_xml_validate_unicode(uint32_t val);

size_t modp_xml_unicode_char_to_utf8(char* dest, uint32_t uval);

uint32_t modp_xml_parse_hex_entity(const char* s, size_t len);

/**
 *
 * returns 0 if invalid
 * Exposed for testing
 */
uint32_t modp_xml_parse_dec_entity(const char* s, size_t len);

/**
 * Url encode a string.  This uses a very strict definition of url
 * encoding.  The only characters NOT encoded are A-Z, a-z, 0-9, "-",
 * "_", ".", along with the space char getting mapped to "+".
 * Everything else is escaped using "%HEXHEX" format.  This is
 * identical to the implementation of php's urlencode and nearly
 * identical to Java's UrlEncoder class (they do not escape '*' for
 * some reason).
 *
 * \param[out] dest output string.  Must
 * \param[in] str The input string
 * \param[in] len  The length of the input string, excluding any
 *   final null byte.
 */
size_t modp_xml_decode(char* dest, const char* str, size_t len);


END_C

#ifdef __cplusplus
#include <cstring>
#include <string>

namespace modp {

    /**
     * Url decode a string.
     * This function does not allocate memory.
     *
     * \param[in,out] s the string to be decoded
     * \return a reference to the input string.
     *      There is no error case, bad characters are passed through
     */
    inline std::string& xml_decode(std::string& s)
    {
        size_t d = modp_xml_decode(const_cast<char*>(s.data()), s.data(), s.size());
        s.erase(d, std::string::npos);
        return s;
    }

    inline std::string xml_decode(const char* str)
    {
        std::string s(str);
        xml_decode(s);
        return s;
    }

    inline std::string xml_decode(const char* str, size_t len)
    {
        std::string s(str, len);
        xml_decode(s);
        return s;
    }

    inline std::string xml_decode(const std::string& s)
    {
        std::string x(s);
        xml_decode(x);
        return x;
    }
}
#endif

#endif
