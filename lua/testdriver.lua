require 'libinjection'
require 'Test.More'
require 'Test.Builder.Tester'

function print_token_string(tok)
    local out = ''
    if tok.str_open ~= '\0' then
        out = out .. tok.str_open
    end
    out = out .. tok.val
    if tok.str_close ~= '\0' then
        out = out .. tok.str_close
    end
    return(out)
end

function print_token(tok)
   local out = '\n'
   out = out .. tok.type
   out = out .. ' '
   if tok.type == 's' then
       out = out .. print_token_string(tok)
   elseif tok.type == 'v' then
       if tok.count == 1 then
           out = out .. '@'
       elseif tok.count == 2 then
           out = out .. '@@'
       end
       out = out .. print_token_string(tok)
   else
       out = out .. tok.val
   end
   return out
end

function test_tokens(input)
    local out = ''
    local sql_state = libinjection.sfilter()
    local atoken = libinjection.stoken_t()
    libinjection.sqli_init(sql_state, input, input:len(),
                           libinjection.CHAR_NULL, libinjection.COMMENTS_ANSI)
    while (libinjection.sqli_tokenize(sql_state, atoken) == 1) do
        out = out .. print_token(atoken)
    end
    return(out)
end

function test_tokens_mysql(input)
    local out = ''
    local sql_state = libinjection.sfilter()
    local atoken = libinjection.stoken_t()
    libinjection.sqli_init(sql_state, input, input:len(),
                           libinjection.CHAR_NULL, libinjection.COMMENTS_MYSQL)
    while (libinjection.sqli_tokenize(sql_state, atoken) == 1) do
        out = out .. print_token(atoken)
    end
    return(out)
end

function test_folding(input)
    local out = ''
    local sql_state = libinjection.sfilter()
    libinjection.sqli_fingerprint(sql_state, input, input:len(),
                 libinjection.CHAR_NULL, libinjection.COMMENTS_ANSI)
    local vec = sql_state.tokenvec
    for i = 1, sql_state.pat:len() do
        out = out .. print_token(vec[i])
    end
    -- hack for when there is no output
    if out == '' then
        out = '\n'
    end

    return(out)
end

function test_fingerprints(input)
    local out = ''
    local sql_state = libinjection.sfilter()
    local issqli = libinjection.is_sqli(sql_state, input, input:len(), nil)
    if issqli == 1 then
        out = sql_state.pat
    end
    return(out)
end

