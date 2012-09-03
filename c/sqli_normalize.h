#ifndef _SQLPARSE_NORMALIZE_H
#define _SQLPARSE_NORMALIZE_H

/*
 * These are done to prevent editors from being confusing by
 * opening "{" and indenting the whole file
 */

#ifdef __cplusplus
extern "C" {
#endif

#include "modp_stdint.h"

/**
 * Normalizes input string to prepare for SQLi testing:
 *
 *   repeats url decoding until doesn't change
 *   does html unescaping
 *   upper case (ascii only)
 *
 * This modifies the input string and is ALWAYS smaller than original input
 * Ending NULL is added.
 *
 */
size_t sqli_qs_normalize(char *s, size_t slen);

#ifdef __cplusplus
}
#endif

#endif /* _SQLPARSE_NORMALIZE_H */
