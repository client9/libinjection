/* -*- mode: c; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */
#include <stdio.h>
#include "arraytoc.h"

void modp_toupper_map()
{
    size_t i = 0;
    char map[256];
    for (i = 0; i < sizeof(map); ++i) {
        if (i >= 'a' && i <= 'z') {
            map[i] = (char)(i - 32);
        } else {
            map[i] = (char)(i);
        }
    }

    char_array_to_c(map, sizeof(map), "gsToUpperMap");
}


void modp_tolower_map()
{
    size_t i = 0;
    char map[256];
    for (i = 0; i < sizeof(map); ++i) {
        if (i >= 'A' && i <= 'Z') {
            map[i] = (char)(i + 32);
        } else {
            map[i] = (char)i;
        }
    }

    char_array_to_c(map, sizeof(map), "gsToLowerMap");
}

void modp_toprint_map()
{
    size_t i = 0;
    char map[256];
    for (i = 0; i < sizeof(map); ++i) {
        if (i < 32 || i > 126) {
            map[i] = '?';
        } else {
            map[i] = (char) i;
        }
    }

    char_array_to_c(map, sizeof(map), "gsToPrintMap");
}


int main()
{
    modp_toupper_map();
    modp_tolower_map();
    modp_toprint_map();
    return 0;
}
