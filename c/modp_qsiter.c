/* -*- mode: c++; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */

/**
 * \file
 * <pre>
 * modp_qs.c query string key-value pair iterator
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

#include "modp_qsiter.h"

void qsiter_reset(struct qsiter_t* qsi, const char* s, size_t len)
{
    qsi->s = s;
    qsi->len = len;
    qsi->pos = 0;

    qsi->key = NULL;
    qsi->keylen = 0;
    qsi->val = NULL;
    qsi->vallen = 0;
}

bool qsiter_next(struct qsiter_t* qsi)
{
    if (qsi->pos >= qsi->len) {
        qsi->key = NULL;
        qsi->keylen = 0;
        qsi->val = NULL;
        qsi->vallen = 0;
        return false;
    }

    const char* charstart = qsi->s + qsi->pos;
    const char* ends = (const char*) memchr(charstart, '&', qsi->len - qsi->pos);

    if (ends == NULL) {
        const char* eq = (const char*) memchr(charstart, '=', qsi->len - qsi->pos);
        if (eq == NULL) {
            qsi->key = charstart;
            qsi->keylen = (size_t)(qsi->len - qsi->pos);
            qsi->val = NULL;
            qsi->vallen = (size_t)0;
        } else {
            qsi->key = charstart;
            qsi->keylen = (size_t)(eq - charstart);
            qsi->val = eq + 1;
            qsi->vallen = (size_t)((qsi->s + qsi->len) - qsi->val);
        }
        qsi->pos = qsi->len;
        return true;
    } else {
        // &&foo=bar
        const char* eq = (const char*) memchr(charstart, '=', (size_t)(ends - charstart));
        if (eq == NULL) {
            qsi->key = charstart;
            qsi->keylen = (size_t)(ends - charstart);
            qsi->val = NULL;
            qsi->vallen = (size_t)0;
        } else {
            qsi->key = charstart;
            qsi->keylen = (size_t)(eq - charstart);
            qsi->val = eq + 1;
            qsi->vallen = (size_t)(ends - eq - 1);
        }
        qsi->pos = (size_t)((ends - qsi->s) + 1);
        return true;
    }
}
