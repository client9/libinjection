/* -*- mode: c; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */

#include "arraytoc.h"

void hexencodemap()
{
    static const char sHexChars[] = "0123456789ABCDEF";
    int i;
    char hexEncode1[256];
    char hexEncode2[256];
    for (i = 0; i < 256; ++i) {
        hexEncode1[i] = sHexChars[i >> 4];
        hexEncode2[i] = sHexChars[i & 0x0f];
    }

    char_array_to_c(hexEncode1, 256, "gsHexEncodeMap1");
    char_array_to_c(hexEncode2, 256, "gsHexEncodeMap2");
}

void urlencodemap()
{
    uint32_t i;
    char urlEncodeMap[256];

    // 0 means unsafe
    for (i = 0; i < 256; ++i) {
        urlEncodeMap[i] = 0;
    }

    // upper case
    for (i = 'A'; i <= 'Z' ; ++i) {
        urlEncodeMap[i] = (char) i;
    }
    // lower case
    for (i = 'a'; i <= 'z' ; ++i) {
        urlEncodeMap[i] = (char) i;
    }
    // numbers
    for (i = '0'; i <= '9' ; ++i) {
        urlEncodeMap[i] = (char) i;
    }
    // safe chars
    urlEncodeMap[(int)'.'] = '.';
    urlEncodeMap[(int)'-'] = '-';
    urlEncodeMap[(int)'_'] = '_';
    // space is special
    urlEncodeMap[(int)' '] = '+';

    char_array_to_c(urlEncodeMap, 256, "gsUrlEncodeMap");
};

void urlencodeminmap()
{
    int i;
    char urlEncodeMap[256];

    // 0 means unsafe
    for (i = 0; i < 256; ++i) {
        urlEncodeMap[i] = 0;
    }

    // upper case
    for (i = 'A'; i <= 'Z' ; ++i) {
        urlEncodeMap[i] = (char) i;
    }
    // lower case
    for (i = 'a'; i <= 'z' ; ++i) {
        urlEncodeMap[i] = (char) i;
    }
    // numbers
    for (i = '0'; i <= '9' ; ++i) {
        urlEncodeMap[i] = (char) i;
    }

    // space
    urlEncodeMap[(int)' '] = '+';
    const char safechar[] = {'_', '.', '-', '~',
                             '!', '$', '(', ')', '*', ',', ';',
                             ':', '@', '/', '?'};

    int imax = sizeof(safechar);
    for (i = 0; i < imax; ++i) {
        urlEncodeMap[(int)(safechar[i])] = safechar[i];
    }


    char_array_to_c(urlEncodeMap, 256, "gsUrlEncodeMinMap");
};

void hexdecodemap()
{
    uint32_t i;
    uint32_t map[256];
    for (i = 0; i <= 255; ++i) {
        map[i] = 256;
    }

    // digits
    for (i = '0'; i <= '9'; ++i) {
        map[i] = i - '0';
    }

    // upper
    for (i = 'A'; i <= 'F'; ++i) {
        map[i] = i - 'A' + 10;
    }

    // lower
    for (i = 'a'; i <= 'f'; ++i) {
        map[i] = i - 'a' + 10;
    }

    uint32_array_to_c(map, 256, "gsHexDecodeMap");
}

int main()
{
    urlencodemap();
    urlencodeminmap();
    hexdecodemap();
    hexencodemap();
    return 0;
}
