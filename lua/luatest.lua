
require 'libinjection'

dofile('sqlifingerprints.lua')

-- silly callback that just calls back into C
-- identical to libinjection_is_sqli(sql_state, string_input, nil)
--
function check_pattern_c(sqlstate)
    return(libinjection.sqli_blacklist(sqlstate) and
            libinjection.sqli_not_whitelist(sqlstate))
end

-- half lua / half c checker
-- use lua based fingerprint lookup and still uses C code
-- to eliminate false positives
function check_pattern(sqlstate)
    fp = sqlstate.pat
    if sqlifingerprints[fp] == true then
        -- try to eliminate certain false positives
        return(libinjection.sqli_not_whitelist(sqlstate))
    else
        -- not sqli
        return 0
    end
end

-- THIS USES BUILT IN FINGERPRINTS
--  (with last arg of 'nil')

sql_state = libinjection.sfilter()
sqli = '1 union select * from table'
print(libinjection.is_sqli(sql_state, sqli, sqli:len(), nil))
print(sql_state.pat)
print('----')


-- THIS USES LUA FINGERPRINTS via 'check_pattern' function above

for x = 1,2 do
   ok = libinjection.is_sqli(sql_state, sqli, sqli:len(), 'check_pattern')
   if ok == 1 then
      print(sql_state.pat)
      vec = sql_state.tokenvec
      for i = 1, sql_state.pat:len() do
         print(vec[i].type, vec[i].val)
      end
   end
end