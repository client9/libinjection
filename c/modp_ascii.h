/* -*- mode: c++; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */

/**
 * \file modp_ascii.h
 * <PRE>
 * MODP_ASCII -- Simple ascii manipulation (uppercase, lowercase, etc)
 * http://code.google.com/p/stringencoders/
 *
 * Copyright &copy; 2007, Nick Galbreath -- nickg [at] modp [dot] com
 * All rights reserved.
 *
 * Released under bsd license.  See modp_ascii.c for details.
 * </PRE>
 *
 */

#ifndef COM_MODP_STRINGENCODERS_ASCII
#define COM_MODP_STRINGENCODERS_ASCII

#ifdef __cplusplus
#define BEGIN_C extern "C" {
#define END_C }
#else
#define BEGIN_C
#define END_C
#endif

BEGIN_C

/*
 * \param[in,out] str the input string
 * \param[in] len the length of input string (the strlen)
 */
void modp_toupper(char* str, int len);

/** \brief make lower case copy of input string
 *
 * \param[out] output buffer, with at least 'len + 1' bytes allocated
 * \param[in] str the input string
 * \param[in] len the length of input string (the strlen)
 *
 * Please make sure dest has been allocation with at least 'len+1'
 * bytes.  This appends a trailing NULL character at the end of
 * dest!
 *
 * This is based on the algorithm by Paul Hsieh
 * http://www.azillionmonkeys.com/qed/asmexample.html
 */
void modp_toupper_copy(char* dest, const char* str, int len);

/** \brief lower case a string in place
 *
 * \param[in, out] str the input string
 * \param[in] len the length of input string (the strlen)
 *
 */
void modp_tolower(char* str, int len);

/** \brief make lower case copy of input string
 *
 * \param[out] output buffer, with at least 'len + 1' bytes allocated
 * \param[in] str the input string
 * \param[in] len the length of input string (the strlen)
 *
 * Please make sure dest has been allocation with at least 'len+1'
 * bytes.  This appends a trailing NULL character at the end of
 * dest!
 *
 * This is based on the algorithm by Paul Hsieh
 * http://www.azillionmonkeys.com/qed/asmexample.html
 */
void modp_tolower_copy(char* dest, const char* str, int len);

/** \brief turn a string into 7-bit printable ascii.
 *
 * By "printable" we means all characters between 32 and 126.
 * All other values are turned into '?'
 *
 * \param[in, out] str the input string
 * \param[in] len the length of input string (the strlen)
 *
 */
void modp_toprint(char* str, int len);

/** \brief make a printable copy of a string
 *
 * By "printable" we means all characters between 32 and 126.
 * All other values are turned into '?'
 *
 * \param[out] output buffer, with at least 'len + 1' bytes allocated
 * \param[in] str the input string
 * \param[in] len the length of input string (the strlen)
 *
 * Please make sure dest has been allocation with at least 'len+1'
 * bytes.  This appends a trailing NULL character at the end of
 * dest!
 */
void modp_toprint_copy(char* dest, const char* str, int len);

END_C

#ifdef __cplusplus
#include <string>

namespace modp {

    inline std::string& toupper(std::string& str)
    {
        modp_toupper(const_cast<char*>(str.c_str()), str.size());
        return str;
    }

    inline std::string toupper(const std::string& str)
    {
        std::string s(str.size(), '\0');
        modp_toupper_copy(const_cast<char*>(s.data()), str.data(), str.size());
        return s;
    }

    inline std::string tolower(const std::string& str)
    {
        std::string s(str.size(), '\0');
        modp_tolower_copy(const_cast<char*>(s.data()), str.data(), str.size());
        return s;
    }

    inline std::string& tolower(std::string& str)
    {
        modp_tolower(const_cast<char*>(str.c_str()), str.size());
        return str;
    }

    inline std::string toprint(const std::string& str)
    {
        std::string s(str.size(), '\0');
        modp_toprint_copy(const_cast<char*>(s.data()), str.data(), str.size());
        return s;
    }

    inline std::string& toprint(std::string& str)
    {
        modp_toprint(const_cast<char*>(str.c_str()), str.size());
        return str;
    }
}

#endif  /* __cplusplus */

#endif  /* MODP_ASCII */
