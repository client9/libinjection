/* -*- mode: c++; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */

/**
 * \file modp_xml.h
 * \brief Experimental XML/HTML decoder
 *
 * This is mostly experimental.
 */

/*
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
 * \brief Validates a unicode code point is valid for HTML (undefined
 *        or non-white-space control char)
 *
 * \param[in] val a unicode char expressed as a uint32_t
 * \return 0 if invalid, else returns passes back the input value.
 *
 * See http://www.whatwg.org/specs/web-apps/current-work/multipage/syntax.html#character-references for more details
 *
 * This is only exposed for testing.  It is not designed for public use.
 */
uint32_t modp_xml_validate_unicode(uint32_t val);

/**
 * \brief converts a unicode char expressed as uint32_t into a UTF-8 byte sequence.
 * \param[out] dest assumed to have at least 4 chars available in buffer.
 * \param[in] uval A unicode character expressed as a uint32_t type
 * \return 0 if input value is invalid or not a unicode character, else
 *         returns number of bytes written to dest.
 *
 * This is only exposed for testing.  It is not designed for public use.
 */
size_t modp_xml_unicode_char_to_utf8(char* dest, uint32_t uval);

/**
 * \brief parse a hex encoded entity between "&#x" and ";"
 * \param[in] s a buffer pointing at the first char after "&$x"
 * \param[in] len the length of string between "&#x" and ";"
 * \return 0 if invalid
 *
 * This is only exposed for testing.  It is not designed for public use.
 */
uint32_t modp_xml_parse_hex_entity(const char* s, size_t len);

/**
 * \brief parse a numerical decimal XML entity, eg. &x39;
 *
 * \param[in] s the buffer pointing to first char after '&#'.
 * \param[in] len the length between '&#' and ';'.  It is expected
 *            that all chars between are to be decimal digits.
 * \return 0 if invalid, else the value
 *
 * Exposed for testing.  Not designed to be useful for public consumption.
 */
uint32_t modp_xml_parse_dec_entity(const char* s, size_t len);

/**
 * \brief XML decode a string
 * \param[out] dest output string.  Must
 * \param[in] str The input string
 * \param[in] len  The length of the input string, excluding any
 *   final null byte.
 * \return the final size of the output, excluding any ending null byte.
 *
 * Decode numerical entities (decimal or hexadecimal), and following named
 * entities:
 *   * &apos;
 *   * &quot;
 *   * &amp;
 *   * &lt;
 *   * &gt;
 *
 */
size_t modp_xml_decode(char* dest, const char* str, size_t len);

/**
 * \brief XML encode a UTF-8 string
 * \param[out] dest output string.
 * \param[in] str The input string
 * \param[in] len  The length of the input string, excluding any
 *   final null byte.
 * \return the final size of the output, excluding any ending null byte.
 * Encodes an assumed valid UTF-8 input and escapes
 *   * &apos;
 *   * &quot;
 *   * &amp;
 *   * &lt;
 *   * &gt;
 */
size_t modp_xml_encode(char* dest, const char* str, size_t len);

size_t modp_xml_min_encode_strlen(const char* str, size_t len);

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
