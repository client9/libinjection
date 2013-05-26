#!/usr/bin/env python
#
#  Copyright 2012, 2013 Nick Galbreath
#  nickg@client9.com
#  BSD License -- see COPYING.txt for details
#

"""
Data for libinjection.   These are simple data structures
which are exported to JSON.  This is done so comments can be
added to the data directly (JSON doesn't support comments).
"""

KEYWORDS = {
'AUTOINCREMENT'              : 'k',
'UTL_INADDR.GET_HOST_ADDRESS': 'f',

# ORACLE
# http://blog.red-database-security.com/
#  /2009/01/17/tutorial-oracle-sql-injection-in-webapps-part-i/print/
'DBMS_PIPE.RECEIVE_MESSAGE':   'f',
'CTXSYS.DRITHSX.SN': 'f',
'SYS.STRAGG': 'f',
'SYS.FN_BUILTIN_PERMISSIONS'  : 'f',
'SYS.FN_GET_AUDIT_FILE'       : 'f',
'SYS.FN_MY_PERMISSIONS'       : 'f',
'ABORT'                       : 'k',
'ABS'                         : 'f',
'ACCESSIBLE'                  : 'k',
'ACOS'                        : 'f',
'ADD'                         : 'k',
'ADDDATE'                     : 'f',
'ADDTIME'                     : 'f',
'AES_DECRYPT'                 : 'f',
'AES_ENCRYPT'                 : 'f',
'AGAINST'                     : 'k',
'AGE'                         : 'f',
'ALTER'                       : 'k',

# 'ALL_USERS' - oracle
'ALL_USERS'                   : 'k',

'ANALYZE'                     : 'k',
'AND'                         : '&',
# array_... pgsql
'ARRAY_AGG'                   : 'f',
'ARRAY_CAT'                   : 'f',
'ARRAY_NDIMS'                 : 'f',
'ARRAY_DIM'                   : 'f',
'ARRAY_FILL'                  : 'f',
'ARRAY_LENGTH'                : 'f',
'ARRAY_LOWER'                 : 'f',
'ARRAY_UPPER'                 : 'f',
'ARRAY_PREPEND'               : 'f',
'ARRAY_TO_STRING'             : 'f',
'ARRAY_TO_JSON'               : 'f',
'APP_NAME'                    : 'f',
'APPLOCK_MODE'                : 'f',
'APPLOCK_TEST'                : 'f',
'ASSEMBLYPROPERTY'            : 'f',
# too ordinary to be a keyword
'AS'                          : 'n',
'ASC'                         : 'k',
'ASCII'                       : 'f',
'ASENSITIVE'                  : 'k',
'ASIN'                        : 'f',
'ASYMKEY_ID'                  : 'f',
'ATAN'                        : 'f',
'ATAN2'                       : 'f',
'AVG'                         : 'f',
'BEFORE'                      : 'k',
'BEGIN'                       : 'E',
'BENCHMARK'                   : 'f',
'BETWEEN'                     : 'k',
'BIGINT'                      : 'k',
'BIN'                         : 'f',
'BINARY'                      : 'k',
'BINARY_DOUBLE_INFINITY'      : '1',
'BINARY_DOUBLE_NAN'           : '1',
'BINARY_FLOAT_INFINITY'       : '1',
'BINARY_FLOAT_NAN'            : '1',
'BINBINARY'                   : 'f',
'BIT_AND'                     : 'f',
'BIT_COUNT'                   : 'f',
'BIT_LENGTH'                  : 'f',
'BIT_OR'                      : 'f',
'BIT_XOR'                     : 'f',
'BLOB'                        : 'k',
# pgsql
'BOOL_AND'                    : 'f',
# pgsql
'BOOL_OR'                     : 'f',
'BOOLEAN'                     : 'k',
'BOTH'                        : 'k',
# pgsql
'BTRIM'                       : 'f',
'BY'                          : 'n',

# MS ACCESS
#
#
'CBOOL'                       : 'f',
'CBYTE'                       : 'f',
'CCUR'                        : 'f',
'CDATE'                       : 'f',
'CDBL'                        : 'f',
'CINT'                        : 'f',
'CLNG'                        : 'f',
'CSNG'                        : 'f',
'CVAR'                        : 'f',
# CHANGES: sqlite3
'CHANGES'                     : 'f',
'CHDIR'                       : 'f',
'CHDRIVE'                     : 'f',
'CURDIR'                      : 'f',
'FILEDATETIME'                : 'f',
'FILELEN'                     : 'f',
'GETATTR'                     : 'f',
'MKDIR'                       : 'f',
'SETATTR'                     : 'f',
'DAVG'                        : 'f',
'DCOUNT'                      : 'f',
'DFIRST'                      : 'f',
'DLAST'                       : 'f',
'DLOOKUP'                     : 'f',
'DMAX'                        : 'f',
'DMIN'                        : 'f',
'DSUM'                        : 'f',

'CALL'                        : 'k',
'CASCADE'                     : 'k',
'CASE'                        : 'E',
'CAST'                        : 'f',
# pgsql 'cube root' lol
'CBRT'                        : 'f',
'CEIL'                        : 'f',
'CEILING'                     : 'f',
'CERTENCODED'                 : 'f',
'CERTPRIVATEKEY'              : 'f',
'CERT_ID'                     : 'f',
'CERT_PROPERTY'               : 'f',
'CHANGE'                      : 'k',

# 'CHAR'
# sometimes a function too
'CHAR'                        : 'f',

'CHARACTER'                   : 'k',
'CHARACTER_LENGTH'            : 'f',
'CHARINDEX'                   : 'f',
'CHARSET'                     : 'f',
'CHAR_LENGTH'                 : 'f',
'CHECK'                       : 'k',
'CHECKSUM_AGG'                : 'f',
'CHOOSE'                      : 'f',
'CHR'                         : 'f',
'CLOCK_TIMESTAMP'             : 'f',
'COALESCE'                    : 'k',
'COERCIBILITY'                : 'f',
'COL_LENGTH'                  : 'f',
'COL_NAME'                    : 'f',
'COLLATE'                     : 'k',
'COLLATION'                   : 'f',
'COLLATIONPROPERTY'           : 'f',

# TBD
'COLUMN'                      : 'k',

'COLUMNPROPERTY'              : 'f',
'COLUMNS_UPDATED'             : 'f',
'COMPRESS'                    : 'f',
'CONCAT'                      : 'f',
'CONCAT_WS'                   : 'f',
'CONDITION'                   : 'k',
'CONNECTION_ID'               : 'f',
'CONSTRAINT'                  : 'k',
'CONTINUE'                    : 'k',
'CONV'                        : 'f',
'CONVERT'                     : 'f',
# pgsql
'CONVERT_FROM'                : 'f',
# pgsql
'CONVERT_TO'                  : 'f',
'CONVERT_TZ'                  : 'f',
'COS'                         : 'f',
'COT'                         : 'f',
'COUNT'                       : 'f',
'COUNT_BIG'                   : 'k',
'CRC32'                       : 'f',
'CREATE'                      : 'E',
'CROSS'                       : 'n',
'CUME_DIST'                   : 'f',
'CURDATE'                     : 'f',

# TBD
'CURRENT_DATE'                : 'k',
'CURRENT_DATABASE'            : 'f',
# TBD
'CURRENT_TIME'                : 'k',
# TBD
'CURRENT_TIMESTAMP'           : 'k',
'CURRENT_QUERY'               : 'f',
'CURRENT_SCHEMA'              : 'f',
'CURRENT_SCHEMAS'             : 'f',
'CURRENT_SETTING'             : 'p',
# TBD
'CURRENT_USER'                : 'k',
'CURRENTUSER'                 : 'f',
# pgsql
'CURRVAL'                     : 'f',
'CURSOR'                      : 'k',
'CURSOR_STATUS'               : 'f',
'CURTIME'                     : 'f',

# this might be a function
'DATABASE'                    : 'n',
'DATABASE_PRINCIPAL_ID'       : 'f',
'DATABASEPROPERTYEX'          : 'f',
'DATABASES'                   : 'k',
'DATALENGTH'                  : 'f',
'DATE'                        : 'f',
'DATEDIFF'                    : 'f',
# sqlserver
'DATENAME'                    : 'f',
#sqlserver
'DATEPART'                    : 'f',
'DATEADD'                     : 'f',
'DATESERIAL'                  : 'f',
'DATEVALUE'                   : 'f',
'DATEFROMPARTS'               : 'f',
'DATETIME2FROMPARTS'          : 'f',
'DATETIMEFROMPARTS'           : 'f',
# sqlserver
'DATETIMEOFFSETFROMPARTS'     : 'f',
'DATE_ADD'                    : 'f',
'DATE_FORMAT'                 : 'f',
'DATE_PART'                   : 'f',
'DATE_SUB'                    : 'f',
'DATE_TRUNC'                  : 'f',
'DAY'                         : 'f',
'DAYNAME'                     : 'f',
'DAYOFMONTH'                  : 'f',
'DAYOFWEEK'                   : 'f',
'DAYOFYEAR'                   : 'f',
'DAY_HOUR'                    : 'k',
'DAY_MICROSECOND'             : 'k',
'DAY_MINUTE'                  : 'k',
'DAY_SECOND'                  : 'k',
'DB_ID'                       : 'f',
'DB_NAME'                     : 'f',
'DEC'                         : 'k',
'DECIMAL'                     : 'k',
'DECLARE'                     : 'E',
'DECODE'                      : 'f',
'DECRYPTBYASMKEY'             : 'f',
'DECRYPTBYCERT'               : 'f',
'DECRYPTBYKEY'                : 'f',
'DECRYPTBYKEYAUTOCERT'        : 'f',
'DECRYPTBYPASSPHRASE'         : 'f',
'DEFAULT'                     : 'k',
'DEGREES'                     : 'f',
'DELAY'                       : 'k',
'DELAYED'                     : 'k',
'DELETE'                      : 'k',
'DENSE_RANK'                  : 'f',
'DESC'                        : 'k',
'DESCRIBE'                    : 'k',
'DES_DECRYPT'                 : 'f',
'DES_ENCRYPT'                 : 'f',
'DETERMINISTIC'               : 'k',
'DIFFERENCE'                  : 'f',
'DISTINCROW'                  : 'k',
'DISTINCT'                    : 'k',
'DIV'                         : 'o',
'DROP'                        : 'E',
'DUAL'                        : 'k',
'EACH'                        : 'k',
'ELSE'                        : 'k',
'ELSEIF'                      : 'k',
'ELT'                         : 'f',
'ENCLOSED'                    : 'k',
'ENCODE'                      : 'f',
'ENCRYPT'                     : 'f',
'ENCRYPTBYASMKEY'             : 'f',
'ENCRYPTBYCERT'               : 'f',
'ENCRYPTBYKEY'                : 'f',
'ENCRYPTBYPASSPHRASE'         : 'f',

#
# sqlserver
'EOMONTH'                     : 'f',

# pgsql
'ENUM_FIRST'                  : 'f',
'ENUM_LAST'                   : 'f',
'ENUM_RANGE'                  : 'f',

'ESCAPED'                     : 'k',

# TBD
#'END'                         : 'k',

# 'EXEC' - MSSQL
#
'EXEC'                        : 'E',
'EXECUTE'                     : 'k',
'EXISTS'                      : 'k',
'EXIT'                        : 'k',
'EXP'                         : 'f',
'EXPLAIN'                     : 'k',
'EXPORT_SET'                  : 'f',
'EXTRACT'                     : 'f',
'EXTRACTVALUE'                : 'f',
'EXTRACT_VALUE'               : 'f',
'EVENTDATA'                   : 'f',
'FALSE'                       : '1',
'FETCH'                       : 'k',
'FIELD'                       : 'f',
'FILE_ID'                     : 'f',
'FILE_IDEX'                   : 'f',
'FILE_NAME'                   : 'f',
'FILEGROUP_ID'                : 'f',
'FILEGROUP_NAME'              : 'f',
'FILEGROUPPROPERTY'           : 'f',
'FILEPROPERTY'                : 'f',
'FIND_IN_SET'                 : 'f',
'FIRST_VALUE'                 : 'f',
'FLOOR'                       : 'f',
'FN_VIRTUALFILESTATS'         : 'f',
'FORCE'                       : 'k',
'FOREIGN'                     : 'k',
'FOR'                         : 'n',
'FORMAT'                      : 'f',
'FOUND_ROWS'                  : 'f',
'FROM'                        : 'k',
'FROM_DAYS'                   : 'f',
'FROM_UNIXTIME'               : 'f',
'FULLTEXT'                    : 'k',
'FULLTEXTCATALOGPROPERTY'     : 'f',
'FULLTEXTSERVICEPROPERTY'     : 'f',
# pgsql
'GENERATE_SERIES'             : 'f',
# pgsql
'GENERATE_SUBSCRIPTS'         : 'f',
# sqlserver
'GETDATE'                     : 'f',
# sqlserver
'GETUTCDATE'                  : 'f',
# pgsql
'GET_BIT'                     : 'f',
# pgsql
'GET_BYTE'                    : 'f',
'GET_FORMAT'                  : 'f',
'GET_LOCK'                    : 'f',
'GOTO'                        : 'k',
'GRANT'                       : 'k',
'GREATEST'                    : 'f',
'GROUP'                       : 'n',
'GROUPING'                    : 'f',
'GROUPING_ID'                 : 'f',
'GROUP_CONCAT'                : 'f',

'HAS_PERMS_BY_NAME'           : 'f',
'HASHBYTES'                   : 'f',
#
# 'HAVING' - MSSQL
'HAVING'                      : 'k',

'HEX'                         : 'f',
'HIGH_PRIORITY'               : 'k',
'HOUR'                        : 'f',
'HOUR_MICROSECOND'            : 'k',
'HOUR_MINUTE'                 : 'k',
'HOUR_SECOND'                 : 'k',

# 'HOST_NAME' -- transact-sql
'HOST_NAME'                   : 'f',

'IDENT_CURRENT'               : 'f',
'IDENT_INCR'                  : 'f',
'IDENT_SEED'                  : 'f',
'IDENTIFY'                    : 'f',

# 'IF - if is normally a function, except in TSQL
# http://msdn.microsoft.com/en-us/library/ms182717.aspx
'IF'                          : 'E',

'IFF'                         : 'f',
'IFNULL'                      : 'f',
'IGNORE'                      : 'k',
'IIF'                         : 'f',

# IN is a special case.. sometimes a function, sometimes a keyword
# corrected inside the folding code
'IN'                          : 'n',

'INDEX'                       : 'k',
'INDEX_COL'                   : 'f',
'INDEXKEY_PROPERTY'           : 'f',
'INDEXPROPERTY'               : 'f',
'INET_ATON'                   : 'f',
'INET_NTOA'                   : 'f',
'INFILE'                      : 'k',
# pgsql
'INITCAP'                     : 'f',
'INNER'                       : 'k',
'INOUT'                       : 'k',
'INSENSITIVE'                 : 'k',
'INSERT'                      : 'E',
'INSTR'                       : 'f',
'INSTRREV'                    : 'f',
'INT'                         : 'k',
'INT1'                        : 'k',
'INT2'                        : 'k',
'INT3'                        : 'k',
'INT4'                        : 'k',
'INT8'                        : 'k',
'INTEGER'                     : 'k',
'INTERVAL'                    : 'k',
'INTO'                        : 'k',
'IS'                          : 'o',
 #sqlserver
'ISDATE'                      : 'f',
'ISEMPTY'                     : 'f',
# pgsql
'ISFINITE'                    : 'f',
'ISNULL'                      : 'f',
'ISNUMERIC'                   : 'f',
'IS_FREE_LOCK'                : 'f',
#
# 'IS_MEMBER' - MSSQL
'IS_MEMBER'                   : 'f',
'IS_ROLEMEMBER'               : 'f',
'IS_OBJECTSIGNED'             : 'f',
# 'IS_SRV...' MSSQL
'IS_SRVROLEMEMBER'            : 'f',
'IS_USED_LOCK'                : 'f',
'ITERATE'                     : 'k',
'JOIN'                        : 'k',
'JULIANDAY'                   : 'f',
# pgsql
'JUSTIFY_DAYS'                : 'f',
'JUSTIFY_HOURS'               : 'f',
'JUSTIFY_INTERVAL'            : 'f',
'KEY_ID'                      : 'f',
'KEY_GUID'                    : 'f',
'KEYS'                        : 'k',
'KILL'                        : 'k',
'LAG'                         : 'f',
'LAST_INSERT_ID'              : 'f',
'LAST_INSERT_ROWID'           : 'f',
'LAST_VALUE'                  : 'f',
'LASTVAL'                     : 'f',
'LCASE'                       : 'f',
'LEAD'                        : 'f',
'LEADING'                     : 'k',
'LEAST'                       : 'f',
'LEAVE'                       : 'k',
'LEFT'                        : 'n',
'LENGTH'                      : 'f',
'LIKE'                        : 'o',
'LIMIT'                       : 'k',
'LINEAR'                      : 'k',
'LINES'                       : 'k',
'LN'                          : 'f',
'LOAD'                        : 'k',
'LOAD_EXTENSION'              : 'f',
'LOAD_FILE'                   : 'f',
'LOCALTIME'                   : 'k',
'LOCALTIMESTAMP'              : 'k',
'LOCATE'                      : 'f',
'LOCK'                        : 'n',
'LOG'                         : 'f',
'LOG10'                       : 'f',
'LOG2'                        : 'f',
'LONGBLOB'                    : 'k',
'LONGTEXT'                    : 'k',
'LOOP'                        : 'k',
'LOWER'                       : 'f',
'LOWER_INC'                   : 'f',
'LOWER_INF'                   : 'f',
'LOW_PRIORITY'                : 'k',
'LPAD'                        : 'f',
'LTRIM'                       : 'f',
'MAKEDATE'                    : 'f',
'MAKE_SET'                    : 'f',
'MASKLEN'                     : 'f',
'MASTER_BIND'                 : 'k',
'MASTER_POS_WAIT'             : 'f',
'MASTER_SSL_VERIFY_SERVER_CERT': 'k',
'MATCH'                       : 'k',
'MAX'                         : 'f',
'MAXVALUE'                    : 'k',
'MD5'                         : 'f',
'MEDIUMBLOB'                  : 'k',
'MEDIUMINT'                   : 'k',
'MEDIUMTEXT'                  : 'k',
'MERGE'                       : 'k',
'MICROSECOND'                 : 'f',
'MID'                         : 'f',
'MIDDLEINT'                   : 'k',
'MIN'                         : 'f',
'MINUTE'                      : 'f',
'MINUTE_MICROSECOND'          : 'k',
'MINUTE_SECOND'               : 'k',
'MOD'                         : 'o',
'MODE'                        : 'n',
'MODIFIES'                    : 'k',
'MONTH'                       : 'f',
'MONTHNAME'                   : 'f',
'NAME_CONST'                  : 'f',
'NATURAL'                     : 'n',
'NETMASK'                     : 'f',
'NEXTVAL'                     : 'f',
'NOT'                         : 'o',
'NOTNULL'                     : 'k',
'NOW'                         : 'f',
'NO_WRITE_TO_BINLOG'          : 'k',
'NTH_VALUE'                   : 'f',
'NTILE'                       : 'f',

# NULL is treated as "variable" type
# Sure it's a keyword, but it's really more
# like a number or value.
# but we don't want it folded away
# since it's a good indicator of SQL
# ('true' and 'false' are also similar)
'NULL'                        : 'v',

'NULLIF'                      : 'f',
'NUMERIC'                     : 'k',
# MSACCESS
'NZ'                          : 'f',
'OBJECT_DEFINITION'           : 'f',
'OBJECT_ID'                   : 'f',
'OBJECT_NAME'                 : 'f',
'OBJECT_SCHEMA_NAME'          : 'f',
'OBJECTPROPERTY'              : 'f',
'OBJECTPROPERTYEX'            : 'f',
'OCT'                         : 'f',
'OCTET_LENGTH'                : 'f',
'OFFSET'                      : 'k',
'OLD_PASSWORD'                : 'f',

# need to investigate how used
#'ON'                          : 'k',
'ONE_SHOT'                    : 'k',

# obviously not SQL but used in attacks
'OWN3D'                       : 'k',

# 'OPEN'
# http://msdn.microsoft.com/en-us/library/ms190500.aspx
'OPEN'                        : 'k',
# 'OPENDATASOURCE'
# http://msdn.microsoft.com/en-us/library/ms179856.aspx
'OPENDATASOURCE'              : 'f',
'OPENXML'                     : 'f',
'OPENQUERY'                   : 'f',
'OPENROWSET'                  : 'f',
'OPTIMIZE'                    : 'k',
'OPTION'                      : 'k',
'OPTIONALLY'                  : 'k',
'OR'                          : '&',
'ORD'                         : 'f',
'ORDER'                       : 'n',
'ORIGINAL_DB_NAME'            : 'f',
'ORIGINAL_LOGIN'              : 'f',
'OUT'                         : 'k',
'OUTER'                       : 'n',
'OUTFILE'                     : 'k',
# unusual PGSQL operator that looks like a function
'OVERLAPS'                    : 'f',
# pgsql
'OVERLAY'                     : 'f',
'PARSENAME'                   : 'f',
'PARTITION'                   : 'k',

# keyword "SET PASSWORD", and a function
'PASSWORD'                    : 'n',
'PATINDEX'                    : 'f',
'PATHINDEX'                   : 'f',
'PERCENT_RANK'                : 'f',
'PERCENTILE_COUNT'            : 'f',
'PERCENTILE_DISC'             : 'f',
'PERCENTILE_RANK'             : 'f',
'PERIOD_ADD'                  : 'f',
'PERIOD_DIFF'                 : 'f',
'PERMISSIONS'                 : 'f',
'PG_ADVISORY_LOCK'            : 'f',
'PG_BACKEND_PID'              : 'f',
'PG_CANCEL_BACKEND'           : 'f',
'PG_CREATE_RESTORE_POINT'     : 'f',
'PG_RELOAD_CONF'              : 'f',
'PG_CLIENT_ENCODING'          : 'f',
'PG_CONF_LOAD_TIME'           : 'f',
'PG_LISTENING_CHANNELS'       : 'f',
'PG_HAS_ROLE'                 : 'f',
'PG_IS_IN_RECOVERY'           : 'f',
'PG_IS_OTHER_TEMP_SCHEMA'     : 'f',
'PG_LS_DIR'                   : 'f',
'PG_MY_TEMP_SCHEMA'           : 'f',
'PG_POSTMASTER_START_TIME'    : 'f',
'PG_READ_FILE'                : 'f',
'PG_READ_BINARY_FILE'         : 'f',
'PG_ROTATE_LOGFILE'           : 'f',
'PG_STAT_FILE'                : 'f',
'PG_SLEEP'                    : 'f',
'PG_START_BACKUP'             : 'f',
'PG_STOP_BACKUP'              : 'f',
'PG_SWITCH_XLOG'              : 'f',
'PG_TERMINATE_BACKEND'        : 'f',
'PG_TRIGGER_DEPTH'            : 'f',
'PI'                          : 'f',
'POSITION'                    : 'f',
'POW'                         : 'f',
'POWER'                       : 'f',
'PRECISION'                   : 'k',
'PRIMARY'                     : 'k',
'PROCEDURE'                   : 'k',
'PUBLISHINGSERVERNAME'        : 'f',
'PURGE'                       : 'k',
'PWDCOMPARE'                  : 'f',
'PWDENCRYPT'                  : 'f',
'QUARTER'                     : 'f',
'QUOTE'                       : 'f',
# pgsql
'QUOTE_IDENT'                 : 'f',
'QUOTENAME'                   : 'f',
# pgsql
'QUOTE_LITERAL'               : 'f',
# pgsql
'QUOTE_NULLABLE'              : 'f',
'RADIANS'                     : 'f',
'RAND'                        : 'f',
'RANDOM'                      : 'f',

# 'RANDOMBLOB' - sqlite3
'RANDOMBLOB'                  : 'f',
'RANGE'                       : 'k',
'RANK'                        : 'f',
'READ'                        : 'k',
'READS'                       : 'k',
'READ_WRITE'                  : 'k',

# 'REAL' only used in data definition
'REAL'                        : 'n',
'REFERENCES'                  : 'k',
'REGEXP'                      : 'o',
# pgsql
'REGEXP_REPLACE'              : 'f',
'REGEXP_MATCHES'              : 'f',
'REGEXP_SPLIT_TO_TABLE'       : 'f',
'REGEXP_SPLIT_TO_ARRAY'       : 'f',
'RELEASE'                     : 'k',
'RELEASE_LOCK'                : 'f',
'RENAME'                      : 'k',
'REPEAT'                      : 'k',

# keyword and function
'REPLACE'                     : 'k',
'REPLICATE'                   : 'f',
'REQUIRE'                     : 'k',
'RESIGNAL'                    : 'k',
'RESTRICT'                    : 'k',
'RETURN'                      : 'k',
'REVERSE'                     : 'f',
'REVOKE'                      : 'k',
# RIGHT JOIN vs. RIGHT()
# tricky since it's a function in pgsql
# needs review
'RIGHT'                       : 'n',
'RLIKE'                       : 'o',
'ROUND'                       : 'f',
'ROW'                         : 'f',
'ROW_COUNT'                   : 'f',
'ROW_NUMBER'                  : 'f',
'ROW_TO_JSON'                 : 'f',
'RPAD'                        : 'f',
'RTRIM'                       : 'f',
'SCHEMA'                      : 'k',
'SCHEMA_ID'                   : 'f',
'SCHAMA_NAME'                 : 'f',
'SCHEMAS'                     : 'k',
'SCOPE_IDENTITY'              : 'f',
'SECOND_MICROSECOND'          : 'k',
'SEC_TO_TIME'                 : 'f',
'SELECT'                      : 'E',
'SENSITIVE'                   : 'k',
'SEPARATOR'                   : 'k',
'SESSION_USER'                : 'f',
'SET'                         : 'E',
'SETSEED'                     : 'f',
'SETVAL'                      : 'f',
'SET_BIT'                     : 'f',
'SET_BYTE'                    : 'f',
'SET_CONFIG'                  : 'f',
'SET_MASKLEN'                 : 'f',
'SHA'                         : 'f',
'SHA1'                        : 'f',
'SHA2'                        : 'f',
'SHOW'                        : 'n',
'SHUTDOWN'                    : 'E',
'SIGN'                        : 'f',
'SIGNBYASMKEY'                : 'f',
'SIGNBYCERT'                  : 'f',
'SIGNAL'                      : 'k',
'SIMILAR'                     : 'k',
'SIN'                         : 'f',
'SLEEP'                       : 'f',
#
# sqlserver
'SMALLDATETIMEFROMPARTS'      : 'f',
'SMALLINT'                    : 'k',
'SOUNDEX'                     : 'f',
'SOUNDS'                      : 'o',
'SPACE'                       : 'f',
'SPATIAL'                     : 'k',
'SPECIFIC'                    : 'k',
'SPLIT_PART'                  : 'f',
'SQL'                         : 'k',
'SQLEXCEPTION'                : 'k',
'SQLSTATE'                    : 'k',
'SQLWARNING'                  : 'k',
'SQL_BIG_RESULT'              : 'k',
'SQL_CALC_FOUND_ROWS'         : 'k',
'SQL_SMALL_RESULT'            : 'k',
'SQL_VARIANT_PROPERTY'        : 'f',
'SQRT'                        : 'f',
'SSL'                         : 'k',
'STARTING'                    : 'k',
#pgsql
'STATEMENT_TIMESTAMP'         : 'f',
'STATS_DATE'                  : 'f',
'STDDEV'                      : 'f',
'STDDEV_POP'                  : 'f',
'STDDEV_SAMP'                 : 'f',
'STRAIGHT_JOIN'               : 'k',
'STRCMP'                      : 'f',
'STRCONV'                     : 'f',
# pgsql
'STRING_AGG'                  : 'f',
'STRING_TO_ARRAY'             : 'f',
'STRPOS'                      : 'f',
'STR_TO_DATE'                 : 'f',
'STUFF'                       : 'f',
'SUBDATE'                     : 'f',
'SUBSTR'                      : 'f',
'SUBSTRING'                   : 'f',
'SUBSTRING_INDEX'             : 'f',
'SUBTIME'                     : 'f',
'SUM'                         : 'f',
'SUSER_ID'                    : 'f',
'SUSER_SID'                   : 'f',
'SUSER_SNAME'                 : 'f',
'SUSER_NAME'                  : 'f',
'SYSDATE'                     : 'f',
# sql server
'SYSDATETIME'                 : 'f',
# sql server
'SYSDATETIMEOFFSET'           : 'f',
# 'SYSCOLUMNS'
# http://msdn.microsoft.com/en-us/library/aa26039s8(v=sql.80).aspx
'SYSCOLUMNS'                  : 'k',

# 'SYSOBJECTS'
# http://msdn.microsoft.com/en-us/library/aa260447(v=sql.80).aspx
'SYSOBJECTS'                  : 'k',

# 'SYSUSERS' - MSSQL
# TBD
'SYSUSERS'                    : 'k',
# sqlserver
'SYSUTCDATETME'               : 'f',
'SYSTEM_USER'                 : 'f',
'SWITCHOFFET'                 : 'f',

# 'TABLE'
# because SQLi really can't use 'TABLE'
'TABLE'                       : 'k',
'TAN'                         : 'f',
'TERMINATED'                  : 'k',
'TERTIARY_WEIGHTS'            : 'f',
# TEXTPOS PGSQL 6.0
# remnamed to strpos in 7.0
# http://www.postgresql.org/message-id/20000601091055.A20245@rice.edu
'TEXTPOS'                     : 'f',
'TEXTPTR'                     : 'f',
'TEXTVALID'                   : 'f',
'THEN'                        : 'k',
# TBD
'TIME'                        : 'k',
'TIMEDIFF'                    : 'f',
'TIMEFROMPARTS'               : 'f',
# pgsql
'TIMEOFDAY'                   : 'f',
# ms access
'TIMESERIAL'                  : 'f',
'TIMEVALUE'                   : 'f',
'TIMESTAMP'                   : 'f',
'TIMESTAMPADD'                : 'f',
'TIME_FORMAT'                 : 'f',
'TIME_TO_SEC'                 : 'f',
'TINYBLOB'                    : 'k',
'TINYINT'                     : 'k',
'TINYTEXT'                    : 'k',
#
# sqlserver
'TODATETIMEOFFSET'            : 'f',
# pgsql
'TO_ASCII'                    : 'f',
#
# 'TO_CHAR' -- oracle, pgsql
'TO_CHAR'                     : 'f',
# pgsql
'TO_HEX'                      : 'f',
'TO_DAYS'                     : 'f',
'TO_DATE'                     : 'f',
'TO_NUMBER'                   : 'f',
'TO_SECONDS'                  : 'f',
'TO_TIMESTAMP'                : 'f',
# sqlite3
'TOTAL'                       : 'f',
'TOTAL_CHANGES'               : 'f',
'TOP'                         : 'k',

# 'TRAILING' -- only used in TRIM(TRAILING
# http://www.w3resource.com/sql/character-functions/trim.php
'TRAILING'                    : 'n',
# pgsql
'TRANSACTION_TIMESTAMP'       : 'f',
'TRANSLATE'                   : 'f',
'TRIGGER'                     : 'k',
'TRIGGER_NESTLEVEL'           : 'f',
'TRIM'                        : 'f',
'TRUE'                        : '1',
'TRUNC'                       : 'f',
'TRUNCATE'                    : 'f',
'TRY_CAST'                    : 'f',
'TRY_CONVERT'                 : 'f',
'TRY_PARSE'                   : 'f',
'TYPE_ID'                     : 'f',
'TYPE_NAME'                   : 'f',
'TYPEOF'                      : 'f',
'TYPEPROPERTY'                : 'f',
'UCASE'                       : 'f',
'UNCOMPRESS'                  : 'f',
'UNCOMPRESS_LENGTH'           : 'f',
'UNDO'                        : 'k',
'UNHEX'                       : 'f',
'UNICODE'                     : 'f',
'UNION'                       : 'U',

# 'UNI_ON' -- odd variation that comes up
'UNI_ON'                      : 'U',

# 'UNIQUE'
# only used as a function (DB2) or as "CREATE UNIQUE"
'UNIQUE'                      : 'n',

'UNIX_TIMESTAMP'              : 'f',
'UNLOCK'                      : 'k',
# pgsql
'UNKNOWN'                     : 'k',
'UNNEST'                      : 'f',
'UNSIGNED'                    : 'k',
'UPDATE'                      : 'E',
'UPDATEXML'                   : 'f',
'UPPER'                       : 'f',
'UPPER_INC'                   : 'f',
'UPPER_INF'                   : 'f',
'USAGE'                       : 'k',
'USE'                         : 'E',

# transact-sql function
# however treating as a 'none' type
# since 'user_id' is such a common column name
# TBD
'USER_ID'                     : 'n',
'USER_NAME'                   : 'f',
# 'USER' -- a MySQL function?
#TBD
#'USER'                       : 'n',

'USING'                       : 'f',
# next 3 TBD
'UTC_DATE'                    : 'k',
'UTC_TIME'                    : 'k',
'UTC_TIMESTAMP'               : 'k',
'UUID'                        : 'f',
'UUID_SHORT'                  : 'f',
'VALUES'                      : 'k',
'VARBINARY'                   : 'k',
'VARCHAR'                     : 'k',
'VARCHARACTER'                : 'k',
'VARIANCE'                    : 'f',
'VAR'                         : 'f',
'VARP'                        : 'f',
'VARYING'                     : 'k',
'VAR_POP'                     : 'f',
'VAR_SAMP'                    : 'f',
'VERIFYSIGNEDBYASMKEY'        : 'f',
'VERIFYSIGNEDBYCERT'          : 'f',
'VERSION'                     : 'f',
'WAITFOR'                     : 'n',
'WEEK'                        : 'f',
'WEEKDAY'                     : 'f',
'WEEKDAYNAME'                 : 'f',
'WEEKOFYEAR'                  : 'f',
'WHEN'                        : 'k',
'WHERE'                       : 'k',
'WHILE'                       : 'E',
# pgsql
'WIDTH_BUCKET'                : 'f',
'WITH'                        : 'k',
# XML... oracle, pgsql
'XMLAGG'                      : 'f',
'XMLELEMENT'                  : 'f',
'XMLCOMMENT'                  : 'f',
'XMLCONCAT'                   : 'f',
'XMLFOREST'                   : 'f',
'XMLFORMAT'                   : 'f',
'XMLTYPE'                     : 'f',
'XMLPI'                       : 'f',
'XMLROOT'                     : 'f',
'XMLEXISTS'                   : 'f',
'XML_IS_WELL_FORMED'          : 'f',
'XPATH'                       : 'f',
'XPATH_EXISTS'                : 'f',
'XOR'                         : 'o',
'XP_EXECRESULTSET'            : 'k',
'YEAR'                        : 'f',
'YEARWEEK'                    : 'f',
'YEAR_MONTH'                  : 'k',
'ZEROBLOB'                    : 'f',
'ZEROFILL'                    : 'k'
}

# special in that single char is a valid operator
# special case in that '<=' might also be '<=>'
# ":" isn't an operator in mysql, but other dialects
#   use it.
OPERATORS2 = (
    '!=',   # oracle
    '||',
    '&&',
    '>=',
    '>>',
    '<=',
    '<>',
    ':=',
    '<<',
    '!<', # http://msdn.microsoft.com/en-us/library/ms188074.aspx
    '!>', # http://msdn.microsoft.com/en-us/library/ms188074.aspx
    '+=',
    '-=',
    '*=',
    '/=',
    '%=',
    '|=',
    '&=',
    '^=',
    '|/', # http://www.postgresql.org/docs/9.1/static/functions-math.html
    '!!', # http://www.postgresql.org/docs/9.1/static/functions-math.html
    '~*', # http://www.postgresql.org/docs/9.1/static/functions-matching.html
    '!~', # http://www.postgresql.org/docs/9.1/static/functions-matching.html
    '@>',
    '<@'
    # '!~*'
    )

CHARMAP = [
    'CHAR_WHITE', # 0
    'CHAR_WHITE', # 1
    'CHAR_WHITE', # 2
    'CHAR_WHITE', # 3
    'CHAR_WHITE', # 4
    'CHAR_WHITE', # 5
    'CHAR_WHITE', # 6
    'CHAR_WHITE', # 7
    'CHAR_WHITE', # 8
    'CHAR_WHITE', # 9
    'CHAR_WHITE', # 10
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE', # 20
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE',
    'CHAR_WHITE', # 30
    'CHAR_WHITE', # 31
    'CHAR_WHITE', # 32
    'CHAR_OP2',   # 33 !
    'CHAR_STR',   # 34 "
    'CHAR_COM1',  # 35 "#"
    'CHAR_MONEY', # 36 $
    'CHAR_OP1',   # 37 %
    'CHAR_OP2',   # 38 &
    'CHAR_STR',   # 39 '
    'CHAR_CHAR',  # 40 (
    'CHAR_CHAR',  # 41 )
    'CHAR_OP2',   # 42 *
    'CHAR_OP1',   # 43 +
    'CHAR_CHAR',  # 44 ,
    'CHAR_DASH',  # 45 -
    'CHAR_NUM',   # 46 .
    'CHAR_SLASH', # 47 /
    'CHAR_NUM',   # 48 0
    'CHAR_NUM',   # 49 1
    'CHAR_NUM',   # 50 2
    'CHAR_NUM',   # 51 3
    'CHAR_NUM',   # 52 4
    'CHAR_NUM',   # 53 5
    'CHAR_NUM',   # 54 6
    'CHAR_NUM',   # 55 7
    'CHAR_NUM',   # 56 8
    'CHAR_NUM',   # 57 9
    'CHAR_OP2',  # 58 : colon
    'CHAR_CHAR',  # 59 ; semiclon
    'CHAR_OP2',   # 60 <
    'CHAR_OP2',   # 61 =
    'CHAR_OP2',   # 62 >
    'CHAR_OTHER', # 63 ?   BEEP BEEP
    'CHAR_VAR',   # 64 @
    'CHAR_WORD',  # 65 A
    'CHAR_WORD',  # 66 B
    'CHAR_WORD',  # 67 C
    'CHAR_WORD',  # 68 D
    'CHAR_WORD',  # 69 E
    'CHAR_WORD',  # 70 F
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # Z
    'CHAR_OTHER',           # [
    'CHAR_BACK',            # \\
    'CHAR_OTHER',           # ]
    'CHAR_OP1',             # ^
    'CHAR_WORD',            # _
    'CHAR_TICK',            # 96  backtick `
    'CHAR_WORD',            # 97  a
    'CHAR_WORD',            # 98  b
    'CHAR_WORD',            # 99  c
    'CHAR_WORD',            # 100 d
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',            # @
    'CHAR_WORD',    # 122 z
    'CHAR_OTHER',   # 123 { left brace
    'CHAR_OP2',     # 124 | pipe
    'CHAR_OTHER',   # 125 } right brace
    'CHAR_OP1',     # 126 ~
    'CHAR_WHITE'
]

PHRASES = {
    # pgsql "AT TIME ZONE"
    'AT TIME'           : 'n',
    'AT TIME ZONE'      : 'k',
    'IN BOOLEAN'        : 'n',
    'IN BOOLEAN MODE'   : 'k',
    'IS DISTINCT FROM'  : 'k',
    'IS DISTINCT'       : 'n',
    'IS NOT DISTINCT FROM' : 'k',
    'IS NOT DISTINCT':     'n',
    'CROSS JOIN'        : 'k',
    'ALTER DOMAIN'      : 'k',
    'ALTER TABLE'       : 'k',
    'GROUP BY'          : 'B',
    'ORDER BY'          : 'B',
    'OWN3D BY'          : 'B',
    'SELECT ALL'        : 'E',
    'READ WRITE'        : 'k',

    # 'LOCAL TABLE' pgsql/oracle
    # http://www.postgresql.org/docs/current/static/sql-lock.html
    'LOCK TABLE'        : 'k',

    # 'LOCK TABLES' MYSQL
    #  http://dev.mysql.com/doc/refman/4.1/en/lock-tables.html
    'LOCK TABLES'       : 'k',
    'LEFT OUTER'        : 'k',
    'LEFT JOIN'         : 'k',
    'RIGHT OUTER'       : 'k',
    'RIGHT JOIN'        : 'k',
    'FULL OUTER'        : 'k',
    'NATURAL JOIN'      : 'k',
    'NATURAL INNER'     : 'k',
    'NATURAL OUTER'     : 'k',
    'NATURAL LEFT'      : 'k',
    'NATURAL RIGHT'     : 'k',
    'NATURAL FULL'      : 'k',
    'SOUNDS LIKE'       : 'o',
    'IS NOT'            : 'o',
    'NEXT VALUE'        : 'n',
    'NEXT VALUE FOR'    : 'k',
    'NOT LIKE'          : 'o',
    'NOT BETWEEN'       : 'o',
    'NOT SIMILAR'       : 'o',

    # 'NOT RLIKE' -- MySQL
    'NOT RLIKE'         : 'o',

    'NOT REGEXP'        : 'o',
    'NOT IN'            : 'o',
    'SIMILAR TO'        : 'o',
    'NOT SIMILAR TO'    : 'o',
    'UNION ALL'         : 'U',
    'INTO OUTFILE'      : 'k',
    'WAITFOR DELAY'     : 'E',
    'WAITFOR TIME'      : 'E',
    'WAITFOR RECEIVE'   : 'E',
    'WAITFOR RECEIVE': 'E',
    'CREATE OR REPLACE' : 'E',
    # 'INTERSECT ALL' -- ORACLE
    'INTERSECT ALL'     : 'o',

    # hacker mistake
    'SELECT ALL' : 'E'
    }

import json

def get_fingerprints():
    """
    fingerprints are stored in plain text file, one fingerprint per file
    the result is sorted
    """

    with open('fingerprints.txt', 'r') as lines:
        sqlipat = [ line.strip() for line in lines ]

    return sorted(sqlipat)

def dump():
    """
    generates a JSON file, sorted keys
    """

    objs = {
        'keywords': KEYWORDS,
        'charmap': CHARMAP,
        'operators2': OPERATORS2,
        'phrases': PHRASES,
        'fingerprints': get_fingerprints()
        }
    return json.dumps(objs, sort_keys=True, indent=4)

if __name__ == '__main__':
    print dump()

