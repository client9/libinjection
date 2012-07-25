#!/usr/bin/env python
"""
"""

import re

# o operator
# v variable
# s string
# 1 number
# k keyword
# f function
# c comment
# L (
# R )
# ; ;
# : :
# , ,
# n  none, or name

# don't make method as it's kill performace by 20%
def isWordNumeric(word):
    firstchar = word[0]
    if not (firstchar.isdigit() or firstchar == '.'):
        return False

    # special hexadecimal case
    if word[0:2] == '0X':
        try:
            # TBD, int vs. long in python land
            int(word, 16)
            return True
        except:
            return False

    # float('infinity') is a number
    if word == 'INFINITY':
        return False

    try:
        float(word)
        return True
    except:
        return False

keywords = dict({
'UTL_INADDR.GET_HOST_ADDRESS': 'f',

# http://blog.red-database-security.com/2009/01/17/tutorial-oracle-sql-injection-in-webapps-part-i/print/
'DBMS_PIPE.RECEIVE_MESSAGE':   'f',
'CTXSYS.DRITHSX.SN': 'f',
'SYS.STRAGG': 'f',

'0' : '1',   # quick optimzations for simple numbers
'1' : '1',
'2' : '1',
'3' : '1',
'4' : '1',
'5' : '1',
'6' : '1',
'7' : '1',
'8' : '1',
'9' : '1',
'@'                           : 'n',   # if ' @ '
'@@'                          : 'n',   # if ' @@ '
'ABS'                         : 'f',
'ACCESSIBLE'                  : 'k',
'ACOS'                        : 'f',
'ADD'                         : 'k',
'ADDDATE'                     : 'f',
'ADDTIME'                     : 'f',
'AES_DECRYPT'                 : 'f',
'AES_ENCRYPT'                 : 'f',
'AGAINST'                     : 'k',
'ALTER'                       : 'k',
'ALL_USERS'                   : 'k', # oracle
'ANALYZE'                     : 'k',
'AND'                         : 'o',
'AS'                          : 'k',
'ASC'                         : 'k',
'ASCII'                       : 'f',
'ASENSITIVE'                  : 'k',
'ASIN'                        : 'f',
'ATAN'                        : 'f',
'ATAN2'                       : 'f',
'AVG'                         : 'f',
'BEFORE'                      : 'k',
'BEGIN'                       : 'k',
'BENCHMARK'                   : 'f',
'BETWEEN'                     : 'k',
'BIGINT'                      : 'k',
'BINARY'                      : 'k',
'BINBINARY'                   : 'f',
'BIT_AND'                     : 'f',
'BIT_COUNT'                   : 'f',
'BIT_LENGTH'                  : 'f',
'BIT_OR'                      : 'f',
'BIT_XOR'                     : 'f',
'BLOB'                        : 'k',
'BOOLEAN'                     : 'k',
'BOTH'                        : 'k',
'CALL'                        : 'k',
'CASCADE'                     : 'k',
'CASE'                        : 'o',
'CAST'                        : 'f',
'CEIL'                        : 'f',
'CEILING'                     : 'f',
'CHANGE'                      : 'k',
# sometimes a function too
'CHAR'                        : 'k',

'CHARACTER'                   : 'k',
'CHARACTER_LENGTH'            : 'f',
'CHARSET'                     : 'f',
'CHAR_LENGTH'                 : 'f',
'CHECK'                       : 'k',
'CHR'                         : 'f',
'COALESCE'                    : 'k',
'COERCIBILITY'                : 'f',
'COLLATE'                     : 'k',
'COLLATION'                   : 'f',
'COLUMN'                      : 'k',
'COMPRESS'                    : 'f',
'CONCAT'                      : 'f',
'CONCAT_WS'                   : 'f',
'CONDITION'                   : 'k',
'CONNECTION_ID'               : 'f',
'CONSTRAINT'                  : 'k',
'CONTINUE'                    : 'k',
'CONV'                        : 'f',
'CONVERT'                     : 'f',
'CONVERT_TZ'                  : 'f',
'COS'                         : 'f',
'COT'                         : 'f',
'COUNT'                       : 'f',
'CRC32'                       : 'f',
'CREATE'                      : 'k',
'CURDATE'                     : 'f',
'CURRENT_DATE'                : 'k',
'CURRENT_DATECURRENT_TIME'    : 'f',
'CURRENT_TIME'                : 'k',
'CURRENT_TIMESTAMP'           : 'k',
'CURRENT_USER'                : 'k',
'CURSOR'                      : 'k',
'CURTIME'                     : 'f',
'DATABASE'                    : 'k',
'DATABASES'                   : 'k',
'DATE'                        : 'f',
'DATEDIFF'                    : 'f',
'DATE_ADD'                    : 'f',
'DATE_FORMAT'                 : 'f',
'DATE_SUB'                    : 'f',
'DAY'                         : 'f',
'DAYNAME'                     : 'f',
'DAYOFMONTH'                  : 'f',
'DAYOFWEEK'                   : 'f',
'DAYOFYEAR'                   : 'f',
'DAY_HOUR'                    : 'k',
'DAY_MICROSECOND'             : 'k',
'DAY_MINUTE'                  : 'k',
'DAY_SECOND'                  : 'k',
'DEC'                         : 'k',
'DECIMAL'                     : 'k',
'DECLARE'                     : 'k',
'DECODE'                      : 'f',
'DEFAULT'                     : 'k',
'DEGREES'                     : 'f',
'DELAY'                       : 'k',
'DELAYED'                     : 'k',
'DELETE'                      : 'k',
'DESC'                        : 'k',
'DESCRIBE'                    : 'k',
'DES_DECRYPT'                 : 'f',
'DES_ENCRYPT'                 : 'f',
'DETERMINISTIC'               : 'k',
'DISTINCROW'                  : 'k',
'DISTINCT'                    : 'k',
'DIV'                         : 'o',
'DROP'                        : 'k',
'DUAL'                        : 'k',
'EACH'                        : 'k',
'ELSE'                        : 'k',
'ELSEIF'                      : 'k',
'ELT'                         : 'f',
'ENCLOSED'                    : 'k',
'ENCODE'                      : 'f',
'ENCRYPT'                     : 'f',
'ESCAPED'                     : 'k',
# TBD
#'END'                         : 'k',
'EXEC'                        : 'k',   # mssql
'EXECUTE'                     : 'k',
'EXISTS'                      : 'k',
'EXIT'                        : 'k',
'EXP'                         : 'f',
'EXPLAIN'                     : 'k',
'EXPORT_SET'                  : 'f',
'EXTRACT'                     : 'f',
'EXTRACTVALUE'                : 'f',
'EXTRACT_VALUE'               : 'f',
'FALSE'                       : 'k',
'FETCH'                       : 'k',
'FIELD'                       : 'f',
'FIND_IN_SET'                 : 'f',
'FLOOR'                       : 'f',
'FORCE'                       : 'k',
'FOREIGN'                     : 'k',
'FOR'                         : 'k',
'FORMAT'                      : 'f',
'FOUND_ROWS'                  : 'f',
'FROM'                        : 'k',
'FROM_DAYS'                   : 'f',
'FROM_UNIXTIME'               : 'f',
'FULLTEXT'                    : 'k',
'GENERATE_SERIES'             : 'f',
'GET_FORMAT'                  : 'f',
'GET_LOCK'                    : 'f',
'GOTO'                        : 'k',
'GRANT'                       : 'k',
'GREATEST'                    : 'f',
'GROUP_CONCAT'                : 'f',
'HAVING'                      : 'k',  # MSSQL
'HEX'                         : 'f',
'HIGH_PRIORITY'               : 'k',
'HOUR'                        : 'f',
'HOUR_MICROSECOND'            : 'k',
'HOUR_MINUTE'                 : 'k',
'HOUR_SECOND'                 : 'k',
'HOST_NAME'                   : 'f',  # unknown DB
# if is normally a function, except in TSQL
# http://msdn.microsoft.com/en-us/library/ms182717.aspx
'IF'                          : 'k',
'IFF'                         : 'f',
'IFNULL'                      : 'f',
'IGNORE'                      : 'k',
'IIF'                         : 'f',

# IN is a special case.. sometimes a function, sometimes a keyword
'IN'                          : 'n',

'INDEX'                       : 'k',
'INET_ATON'                   : 'f',
'INET_NTOA'                   : 'f',
'INFILE'                      : 'k',
'INNER'                       : 'k',
'INOUT'                       : 'k',
'INSENSITIVE'                 : 'k',
'INSERT'                      : 'k',
'INSTR'                       : 'f',
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
'ISNULL'                      : 'f',
'IS_FREE_LOCK'                : 'f',
'IS_MEMBER'                   : 'f',  # MSSQL
'IS_SRVROLEMEMBER'            : 'f',  # MSSQL
'IS_USED_LOCK'                : 'f',
'ITERATE'                     : 'k',
'JOIN'                        : 'k',
'KEYS'                        : 'k',
'KILL'                        : 'k',
'LAST_INSERT_ID'              : 'f',
'LCASE'                       : 'f',
'LEADING'                     : 'k',
'LEAST'                       : 'f',
'LEAVE'                       : 'k',
'LEFT'                        : 'f',
'LENGTH'                      : 'f',
'LIKE'                        : 'o',
'LIMIT'                       : 'k',
'LINEAR'                      : 'k',
'LINES'                       : 'k',
'LN'                          : 'f',
'LOAD'                        : 'k',
'LOAD_FILE'                   : 'f',
'LOCALTIME'                   : 'k',
'LOCALTIMESTAMP'              : 'k',
'LOCATE'                      : 'f',
'LOCK'                        : 'k',
'LOG'                         : 'f',
'LOG10'                       : 'f',
'LOG2'                        : 'f',
'LONGBLOB'                    : 'k',
'LONGTEXT'                    : 'k',
'LOOP'                        : 'k',
'LOWER'                       : 'f',
'LOW_PRIORITY'                : 'k',
'LPAD'                        : 'f',
'LTRIM'                       : 'f',
'MAKEDATE'                    : 'f',
'MAKE_SET'                    : 'f',
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
'NOT'                         : 'o',
'NOW'                         : 'f',
'NO_WRITE_TO_BINLOG'          : 'k',
'NULL'                        : '1',
'NULLIF'                      : 'f',
'NUMERIC'                     : 'k',
'OCT'                         : 'f',
'OCTET_LENGTH'                : 'f',
'OFFSET'                      : 'k',
'OLD_PASSWORD'                : 'f',
# need to investigate how used
#'ON'                          : 'k',
'ONE_SHOT'                    : 'k',
# obviously not SQL but used in attacks
'OWN3D'                       : 'k',
'OPEN'                        : 'k', # http://msdn.microsoft.com/en-us/library/ms190500.aspx
'OPENDATASOURCE'              : 'f', # http://msdn.microsoft.com/en-us/library/ms179856.aspx
'OPENXML'                     : 'f',
'OPENQUERY'                   : 'f',
'OPENROWSET'                  : 'f',
'OPTIMIZE'                    : 'k',
'OPTION'                      : 'k',
'OPTIONALLY'                  : 'k',
'OR'                          : 'o',
'ORD'                         : 'f',
'OUT'                         : 'k',
'OUTFILE'                     : 'k',
'PARTITION'                   : 'k',
'PASSWORD'                    : 'k',  # keyword "SET PASSWORD", and a function
'PERIOD_ADD'                  : 'f',
'PERIOID_DIFF'                : 'f',
'PG_SLEEP'                    : 'f',
'PI'                          : 'f',
'POSITION'                    : 'f',
'POW'                         : 'f',
'POWER'                       : 'f',
'PRECISION'                   : 'k',
'PRIMARY'                     : 'k',
'PROCEDURE'                   : 'k',
'PURGE'                       : 'k',
'QUARTER'                     : 'f',
'QUOTE'                       : 'f',
'RADIANS'                     : 'f',
'RAND'                        : 'f',
'RANDOMBLOB'                  : 'f',  # sqlite3
'RANGE'                       : 'k',
'READ'                        : 'k',
'READS'                       : 'k',
'READ_WRITE'                  : 'k',
'REAL'                        : 'n',   # only used in data definition
'REFERENCES'                  : 'k',
'REGEXP'                      : 'o',
'RELEASE'                     : 'k',
'RELEASE_LOCK'                : 'f',
'RENAME'                      : 'k',
'REPEAT'                      : 'k',
'REPLACE'                     : 'k',
'REQUIRE'                     : 'k',
'RESIGNAL'                    : 'k',
'RESTRICT'                    : 'k',
'RETURN'                      : 'k',
'REVERSE'                     : 'f',
'REVOKE'                      : 'k',
'RIGHT'                       : 'f',
'RLIKE'                       : 'o',
'ROUND'                       : 'f',
'ROW'                         : 'f',
'ROW_COUNT'                   : 'f',
'RPAD'                        : 'f',
'RTRIM'                       : 'f',
'SCHEMA'                      : 'k',
'SCHEMAS'                     : 'k',
'SECOND_MICROSECOND'          : 'k',
'SEC_TO_TIME'                 : 'f',
'SELECT'                      : 'k',
'SENSITIVE'                   : 'k',
'SEPARATOR'                   : 'k',
'SESSION_USER'                : 'f',
'SET'                         : 'k',
'SHA'                         : 'f',
'SHA1'                        : 'f',
'SHA2'                        : 'f',
'SHOW'                        : 'k',
'SHUTDOWN'                    : 'k',
'SIGN'                        : 'f',
'SIGNAL'                      : 'k',
'SIMILAR'                     : 'k',
'SIN'                         : 'f',
'SLEEP'                       : 'f',
'SMALLINT'                    : 'k',
'SOUNDEX'                     : 'f',
'SOUNDS'                      : 'o',
'SPACE'                       : 'f',
'SPATIAL'                     : 'k',
'SPECIFIC'                    : 'k',
'SQL'                         : 'k',
'SQLEXCEPTION'                : 'k',
'SQLSTATE'                    : 'k',
'SQLWARNING'                  : 'k',
'SQL_BIG_RESULT'              : 'k',
'SQL_CALC_FOUND_ROWS'         : 'k',
'SQL_SMALL_RESULT'            : 'k',
'SQRT'                        : 'f',
'SSL'                         : 'k',
'STARTING'                    : 'k',
'STDDEV'                      : 'f',
'STDDEV_POP'                  : 'f',
'STDDEV_SAMP'                 : 'f',
'STRAIGHT_JOIN'               : 'k',
'STRCMP'                      : 'f',
'STR_TO_DATE'                 : 'f',
'SUBDATE'                     : 'f',
'SUBSTR'                      : 'f',
'SUBSTRING'                   : 'f',
'SUBSTRING_INDEX'             : 'f',
'SUBTIME'                     : 'f',
'SUM'                         : 'f',
'SYSDATE'                     : 'f',
'SYSCOLUMNS'                  : 'k',  # http://msdn.microsoft.com/en-us/library/aa260398(v=sql.80).aspx
'SYSOBJECTS'                  : 'k',  # http://msdn.microsoft.com/en-us/library/aa260447(v=sql.80).aspx
'SYSUSERS'                    : 'k',  # MSSQL
'SYSTEM_USER'                 : 'f',
'TABLE'                       : 'k',
'TAN'                         : 'f',
'TERMINATED'                  : 'k',
'THEN'                        : 'k',
'TIME'                        : 'k',
'TIMEDIFF'                    : 'f',
'TIMESTAMP'                   : 'f',
'TIMESTAMPADD'                : 'f',
'TIME_FORMAT'                 : 'f',
'TIME_TO_SEC'                 : 'f',
'TINYBLOB'                    : 'k',
'TINYINT'                     : 'k',
'TINYTEXT'                    : 'k',
'TO_DAYS'                     : 'f',
'TO_SECONDS'                  : 'f',
'TRAILING'                    : 'k',
'TRIGGER'                     : 'k',
'TRIM'                        : 'f',
'TRUE'                        : 'k',
'TRUNCATE'                    : 'f',
'UCASE'                       : 'f',
'UNCOMPRESS'                  : 'f',
'UNCOMPRESS_LENGTH'           : 'f',
'UNDO'                        : 'k',
'UNHEX'                       : 'f',
'UNION'                       : 'o',
# only used as a function (DB2) or as "CREATE UNIQUE"
'UNIQUE'                      : 'n',
'UNIX_TIMESTAMP'              : 'f',
'UNLOCK'                      : 'k',
'UNSIGNED'                    : 'k',
'UPDATE'                      : 'k',
'UPDATEXML'                   : 'f',
'UPPER'                       : 'f',
'USAGE'                       : 'k',
'USE'                         : 'k',
#'USER'                       : 'k',   # MySQL function?
'USING'                       : 'f',
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
'VARYING'                     : 'k',
'VAR_POP'                     : 'f',
'VAR_SAMP'                    : 'f',
'VERSION'                     : 'f',
'WAITFOR'                     : 'k',
'WEEK'                        : 'f',
'WEEKDAY'                     : 'f',
'WEEKOFYEAR'                  : 'f',
'WHEN'                        : 'k',
'WHERE'                       : 'k',
'WHILE'                       : 'k',
'WITH'                        : 'k',
'XMLELEMENT'                  : 'f',   # oracle
'XMLFOREST'                   : 'f',   # oracle
'XMLFORMAT'                   : 'f',   # oracle
'XMLTYPE'                     : 'f',
'XOR'                         : 'o',
'XP_EXECRESULTSET'            : 'k',
'YEAR'                        : 'f',
'YEARWEEK'                    : 'f',
'YEAR_MONTH'                  : 'k',
'ZEROFILL'                    : 'k'
})

class SQLexer:
    def __init__(self):

        self.unary_operators = frozenset( (
                '!',
                'NOT',
                '-',
                '+',
                '~'  # bit inversion
                ))

        self.op_chars = "|=&><:*/%^"

        # special in that single char is a valid operator
        # special case in that '<=' might also be '<=>'
        # ":" isn't an operator in mysql, but other dialects
        #   use it.
        self.double_char_operators = frozenset( (
                '!=',   # nonstatndard but common
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
                ) )

        self.keyword_phrases = dict({
                'IN': ('BOOLEAN',),
                'IN BOOLEAN': ('MODE',),
            'ALTER': ('DOMAIN', 'TABLE'),
            'BOOLEAN': ('MODE',),
            'GROUP': ('BY',),
            'ORDER': ('BY',),
            'OWN3D': ('BY',),
            'SELECT': ('ALL',),
            'READ': ('WRITE',),
            'LEFT': ('OUTER', 'JOIN'),
            'RIGHT': ('OUTER', 'JOIN'),
            'FULL': ('OUTER',),
            'CROSS': ('JOIN'),
            'NATURAL': ('JOIN','INNER', 'OUTER','LEFT', 'RIGHT', 'FULL')
            })

        self.operator_phrases = dict({
            'SOUNDS': ('LIKE',),
            'IS': ('NOT',),
            'NOT': ('LIKE', 'BETWEEN', 'SIMILAR'),
            'SIMILAR': ('TO',),
            'NOT SIMILAR': ('TO',),
            'UNION': ('ALL',)
            })

        self.re_singleq = re.compile(r"[^\\]'", re.MULTILINE)
        self.re_doubleq = re.compile(r'[^\\]"', re.MULTILINE)

        # this handles variable types @foo   and foo@bar is not a word
        self.ascii_words_re = re.compile(r'@*[A-Z0-9_.\$]*')

        self.ascii_words = frozenset( (
            '$', '_', '@',
            '0','1','2','3','4','5','6','7','8','9',
            'A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '.'  # special case
            ) )

        self.map_main = {
            '~': self.parseSingleCharOperator,
            '^': self.parseSingleCharOperator,
            '+': self.parseSingleCharOperator,

            '*': self.parseSingleCharOperator,

            '%': self.parseSingleCharOperator,

            # double char since we want to eliminate bogus double chars
            '=': self.doubleCharOperator,

            # may be start of single, double or triple operator
            '!': self.doubleCharOperator,

            '&': self.doubleCharOperator,
            '>': self.doubleCharOperator,
            '<': self.doubleCharOperator,
            '|': self.doubleCharOperator,
#            ':': self.doubleCharOperator,
            # might "minus" or might be --- comment
            '-': self.parseDashOperator,

            # might be div, or might be '/*'
            '/': self.parseSlashOperator,
            '\\': self.parseBackslashOperator,

            ' ': self.parseWhite,
            "\a": self.parseWhite,
            "\b": self.parseWhite,
            "\f": self.parseWhite,
            "\n": self.parseWhite,
            "\r": self.parseWhite,
            "\t": self.parseWhite,
            "\v": self.parseWhite,

            # what is this next one?
            "\x19": self.parseWhite,

            "#": self.parseEOLComment,
            "'": self.parseString,
            '"': self.parseString,
            '`': self.parseString,
            ',': self.parseComma,
            ';': self.parseSemicolon,
            ':': self.parseColon,
            '(': self.parseLeftParens,
            ')': self.parseRightParens,
            '[': self.parseLeftBracket,
            ']': self.parseRightBracket,
            '{': self.parseNone,
            '}': self.parseNone,
            }

        for i in self.ascii_words:
            self.map_main[i] = self.parseWord

    def tokenize(self, newstr, delim=None):
        map_main = self.map_main

        self.pos = 0
        self.s = newstr
        self.tokens = []

        if delim is not None:
            self.tokens.append(self.parseInitialString(delim))

        while self.pos < len(self.s):
            try:
                parser = map_main[self.s[self.pos]]
                parser()
            except Exception as e:
                self.pos += 1

        return self.tokens

    def parseWhite(self):
        """ just skips """
        self.pos += 1

    def parseComma(self):
        """ just skips """
        self.tokens.append( (',', ',') )
        self.pos += 1

    def parseNone(self):
        """ just skips """
        self.tokens.append( ('n', self.s[self.pos]) )
        self.pos += 1

    def parseSemicolon(self):
        """ just skips """
        self.tokens.append( (';', ';') )
        self.pos += 1

    def parseColon(self):
        """ just skips """
        self.tokens.append( (':', ':') )
        self.pos += 1

    def parseLeftParens(self):
        """ just skips """
        self.tokens.append( ('L', '(') )
        self.pos += 1

    def parseLeftBracket(self):
        """ just skips """
        self.tokens.append( ('[', '[') )
        self.pos += 1

    def parseRightBracket(self):
        """ just skips """
        self.tokens.append( (']', ']') )
        self.pos += 1

    def parseRightParens(self):
        """ just skips """
        self.tokens.append( ('R', ')') )
        self.pos += 1

    def parseEOLComment(self):
        pos = self.pos
        endpos = self.s.find("\n", pos)
        if endpos == -1:
            self.tokens.append( ('c', self.s[pos:]) )
            self.pos = len(self.s)
        else:
            self.tokens.append( ('c', self.s[pos:endpos]) )
            self.pos = endpos + 1

    def parseDashOperator(self):
        pos = self.pos
        if self.s[pos:pos+2] == '--':
            self.pos += 2
            self.parseEOLComment()
        else:
            self.tokens.append( ('o', '-') )
            self.pos += 1

    def parseBackslashOperator(self):
        # http://dev.mysql.com/doc/refman/5.0/en/null-values.html
        if self.s[self.pos+1] == 'N':
            self.tokens.append( ('k', 'NULL') )
            self.pos += 2
            # note "select \Nx" == "select \N as x"
            # not sure it matters
        else:
            self.tokens.append( ('\\', '\\'))
            self.pos += 1

    # return 0 is not a comment
    # return 1 is plain "!" comment
    # return 6 !##### comment
    def isMySQLComment(self):
        offset = 0
        try:
            if self.s[self.pos+2] != '!':
                return 0
            offset = 1
            # do we have a mysql version number?
            # will pop exception if goes past end of line
            # or if not integer
            aint = self.s[self.pos+3:self.pos+8]
            mysqlv = int(aint)
            offset = 6
        except:
            pass

        return offset

    def parseSlashOperator(self):
        # TODO: handle mysql /*! operator
        #   rewrites string

        if self.s[self.pos+1] != '*':
            self.parseSingleCharOperator()
            return

        cstart = self.pos
        inc = self.isMySQLComment()

        # find normal */ closer
        if self.pos+2+inc >= len(self.s):
            endpos = -1
            mysqlcstart = -1
        else:
            endpos = self.s.find('*/', self.pos+2+inc)
            # mysql comments are closed on next opening token
            # /*! foo /*! bar */ ==> foo bar
            mysqlcstart = self.s.find('/*!', self.pos+2+inc)

        if mysqlcstart != -1 and mysqlcstart < endpos:
                # just remove the /*! or /*!00000 and continue
                self.s = self.s[0:self.pos] + ' ' + self.s[self.pos+2+inc:]
                return

        if inc == 0:
            # NORMAL COMMENT
            if endpos == -1:
                # unterminated comment
                self.tokens.append( ('c', self.s[self.pos:]) )
                self.pos = len(self.s)
            else:
                self.tokens.append( ('c', self.s[self.pos:endpos+2]))
                self.pos = endpos + 2
        else:
            # MySQL COMMENT
            if endpos == -1:
                # easy, doesn't terminate
                # just skip over the comment
                self.pos += 2 + inc
            else:
                self.s = self.s[0:self.pos] + ' ' + self.s[self.pos+2+inc : endpos] + ' ' + self.s[endpos+2:]

    def doubleCharOperator(self):
        dco = self.s[self.pos:self.pos+2]

        if dco == '<=' and self.s[self.pos:self.pos+3] == '<=>':
            self.tokens.append( ('o', '<=>') )
            self.pos += 3
        elif dco in self.double_char_operators:
            self.tokens.append( ('o', dco) )
            self.pos += 2
        else:
            self.tokens.append( ('o', dco[0]))
            self.pos += 1

    def parseSingleCharOperator(self):
        cur = self.s[self.pos]
        self.tokens.append( ('o', cur ) )
        self.pos += 1

    def parseWord(self):
        mo = self.ascii_words_re.match(self.s, self.pos)
        word = mo.group()
        self.pos += len(word)

        # instead of making two tokens for "@foo" or "@@foo"
        # merge back into one new type
        wtype = keywords.get(word, None)
        if wtype is not None:
            #if word.startswith('@'):
            self.tokens.append( (wtype, word) )
            return

        if word.startswith('@'):
            self.tokens.append( ('v', word) )
            return

        if isWordNumeric(word):
            self.tokens.append( ('1', word) )
            return

        wtype = 'n'
        if word[0] == '0':
            tmp = word[1:]
            # special case for mysql < 5.1 where /*!0 was indicator
            # of versioned comment. so /*!0FOO*/ => 'FOO'
            # Modern versions of mysql use /*!0FOO*/ ==> 0FOO
            # If we get 0SELECT want to map it back to SELECT

            wtype = keywords.get(tmp, None)
            if wtype is not None:
                word = tmp
            else:
                wtype = 'n'

        self.tokens.append( (wtype, word) )

    def syntax(self, tokens):
        imax = len(tokens)
        if imax == 0:
            return tokens

        cur = 0
        ntokens = []
        lasttoken = None

        # if the snippet starts if a unary operator
        #   if number, convert to a number
        #   if none, function, string, ignore
        if imax > 1 and tokens[0][0] == 'o' and tokens[0][1] in ('+', '-', '~'):
            if tokens[1][0] == '1':
                tokens[1] = ('1', tokens[0][1] + tokens[1][1])
                cur += 1
            elif tokens[1][0] == 'k' and tokens[1][1] in ('TRUE', 'FALSE', 'NULL'):
                cur += 1
            elif tokens[1][0] in ('n', 's', 'c'):
                cur += 1

        while cur < imax:
            thistoken = tokens[cur]
            ttype = thistoken[0]
            tvalue = thistoken[1]

            # skip comments
            if ttype == 'c':
                pass

            # skip strings, keywords, operators
            elif ttype in ('1', 'f', 'v'):
                if lasttoken:
                    ntokens.append(lasttoken)
                    lasttoken = None
                ntokens.append(thistoken)
            elif ttype == 's':
                if lasttoken:
                    if lasttoken[0] == 's':
                        lasttoken = ('s', lasttoken[1] + tvalue)
                    else:
                        ntokens.append(lasttoken)
                        lasttoken = thistoken
                else:
                    lasttoken = thistoken

            # build multi-word operators
            elif ttype == 'o':
                # do we have previous token?
                if lasttoken:
                    if lasttoken[0] == 'o' and lasttoken[1] in self.operator_phrases and thistoken[1] in self.operator_phrases[lasttoken[1]]:
                        ntokens.append( ('o', lasttoken[1] + ' ' + thistoken[1]) )
                        lasttoken = None
                    else:
                        ntokens.append(lasttoken)
                        lasttoken = thistoken
                elif thistoken[1] in self.operator_phrases:
                    lasttoken = thistoken
                else:
                    # hack for case where 'IN' is dual function/keyword
                    ntokens.append(thistoken)
                    lasttoken = None

            # build muli-word keywords
            else:
                # do we have previous token?
                if lasttoken:
                    if lasttoken[1] in self.keyword_phrases and thistoken[1] in self.keyword_phrases[lasttoken[1]]:
                        # this allows 3 word tokens to work
                        lasttoken = ('k', lasttoken[1] + ' ' + thistoken[1])
                        #ntokens.append(lasttoken)
                    elif lasttoken[1] in self.operator_phrases and thistoken[1] in self.operator_phrases[lasttoken[1]]:
                        ntokens.append( ('o', lasttoken[1] + ' ' + thistoken[1]) )
                        lasttoken = None
                    else:
                        if lasttoken == ('n', 'IN'):
                            lasttoken = ('f', 'IN')
                        ntokens.append(lasttoken)
                        lasttoken = thistoken
                elif thistoken[1] in self.keyword_phrases:
                    lasttoken = thistoken
                else:
                    ntokens.append(thistoken)
                    lasttoken = None

            cur += 1

        if lasttoken:
            ntokens.append( lasttoken )

        # finally
        # the last element is a comment, add that.  This for better identification of SQLi attacks
        if tokens[-1][0] == 'c':
            ntokens.append(tokens[-1])

        return ntokens

    def parseInitialString(self, delim):
        while True:
            qpos = self.s.find(delim, self.pos)
            if qpos == -1:
                self.pos = len(self.s)
                word = self.s
                break
            elif qpos == 0:
                word = delim
                self.pos = 1
                break
            elif self.s[qpos-1] == "\\":
                self.pos = qpos+1
            else:
                word = self.s[self.pos:qpos+1]
                self.pos = qpos + 1
                break

        return ('s', word)

    def parseString(self):
        delim = self.s[self.pos]
        while True:
            qpos = self.s.find(delim, self.pos+1)
            if qpos == -1:
                word = self.s[self.pos:]
                self.pos = len(self.s)
                break
            elif self.s[qpos-1] != "\\":
                word = self.s[self.pos:qpos+1]
                self.pos = qpos + 1
                break
            else:
                self.pos = qpos

        self.tokens.append( ('s', word) )



from urllib import unquote, unquote_plus

class Attacker:
    def __init__(self):
        self.lex = SQLexer()
        self.alpha_re = re.compile(r'^\s*[A-Za-z0-9_]*\s*$')

        #  foo10" or foo1'  must start with letter to preven
        #  7" # .... which is likely a measurement, not sqli
        self.alpha_str_re = re.compile(r'^[A-Z][A-Z0-9_]+[\'\"]$')

        self.pmap_new = frozenset(
[
'1ok','1oks,','1oksc','noL1R','1okLk','1okfL',
'sonos', 'sono1', 'sosos', '1ono1',
'sonoo', '1Rono', 's;n:k', 'k1,1,', 'k1,1k',
'nokLk',
# unions
 'okkkn',
'ofL1R',

'fLk,L',
'1,1R,', '1,LfL', '1,Lk1', '1,LkL', '1,Lkf', '1,fL1', '1,sR,', '1;kL1', '1;kLL', '1;kLo', '1;kfL', '1;kks', '1;knL', '1;knc', '1;koL', '1;kok', '1R,L1', '1R;kL', '1R;kf', '1R;kk', '1R;kn', '1R;ko', '1RLRs', '1RR;k', '1RRR;', '1RRRR', '1RRRk', '1RRRo', '1RRk1', '1RRkk', '1RRo1', '1RRoL', '1RRof', '1RRok', '1RRon', '1RRoo', '1Rk1', '1Rk1c', '1Rk1o', '1Rkks', '1Ro1f', '1Ro1k', '1Ro1o', '1RoL1', '1RoLk', '1RoLn', '1RofL', '1Rok1', '1RokL', '1RooL', '1k1', '1k1c', '1kfL1', '1kkL1', '1kksc', '1o1Ro', '1o1fL', '1o1kf', '1o1o1', '1o1oL', '1o1of', '1o1ok', '1o1on', '1o1oo', '1o1ov', '1oL1R', '1oL1o', '1oLL1', '1oLLL', '1oLLf', '1oLfL', '1oLk1', '1oLkf', '1oLkn', '1oLnR', '1oLsR', '1ofL1', '1ofLR', '1ofLf', '1ofLn', '1ok1', '1ok1,', '1ok1c', '1ok1k', '1okL1', '1okv,',
# '1ono1',
 '1onos', '1oo1o', '1ooL1', '1oso1', ';kknc', 'fL1,f', 'fL1Ro', 'fL1o1', 'fLRof', 'fLfL1', 'fLfLR', 'fLkLR', 'fLnLR', 'fLv,1', 'k1kLk', 'k1oLs', 'kLRok', 'kLk,L', 'kLokL', 'kLvvR', 'kfL1,', 'kfL1R', 'kfLfL', 'kfLn,', 'kvkL1', 'n,LfL', 'n,Lk1', 'n,LkL', 'n,Lkf', 'n,fL1', 'n;kL1', 'n;kLL', 'n;kfL', 'n;kks', 'n;knL', 'n;koL', 'n;kok', 'nR;kL', 'nR;kf', 'nR;kk', 'nR;kn', 'nR;ko', 'nRR;k', 'nRRR;', 'nRRRk', 'nRRRo', 'nRRkk', 'nRRo1', 'nRRoL', 'nRRof', 'nRRok', 'nRk1o', 'nRkks', 'nRo1f', 'nRo1o', 'nRoLk', 'nRofL', 'nRokL', 'nkksc', 'no1fL', 'no1o1', 'no1oL', 'no1of', 'noLk1', 'nofL1', 'nokL1', 'noo1o', 'ofL1o', 'ofLRo', 'ok1o1', 'oo1kf', 's,1R,', 's;k1,', 's;k1o', 's;k;', 's;kL1', 's;kLL', 's;kLo', 's;k[k', 's;k[n', 's;kfL', 's;kkn', 's;kks', 's;knL', 's;knc', 's;knk', 's;knn', 's;koL', 's;kok', 'sR,L1', 'sR;kL', 'sR;kf', 'sR;kk', 'sR;kn', 'sR;ko', 'sRR;k', 'sRRR;', 'sRRRk', 'sRRRo', 'sRRk1', 'sRRkk', 'sRRo1', 'sRRoL', 'sRRof', 'sRRok', 'sRRoo', 'sRk1', 'sRk1c', 'sRk1o', 'sRkks', 'sRo1f', 'sRo1k', 'sRo1o', 'sRoLk', 'sRofL', 'sRok1', 'sRokL', 'sRooL', 'sc', 'sfL1R', 'sfLn,', 'sfLsR', 'sk1', 'sk1c', 'sk1o1', 'sk1os', 'skR;k', 'skRk1', 'skRkk', 'skRo1', 'skRoL', 'skRof', 'skRok', 'skks', 'skksc', 'skoL1', 'skoLk', 'so1c', 'so1fL', 'so1kf', 'so1o1', 'so1oL', 'so1of', 'so1ok', 'so1on', 'so1oo', 'so1os', 'so1ov', 'soL1R', 'soL1o', 'soLLL', 'soLLk', 'soLLs', 'soLfL', 'soLk1', 'soLkR', 'soLkk', 'soLkn', 'soLks', 'soLsR', 'sofL1', 'sofLR', 'sofLf', 'sofLk', 'sok1', 'sok1,', 'sok1c', 'sok1o', 'sokL1', 'sokLk', 'sokLo', 'sokLs', 'sokc', 'sokfL', 'sokn,', 'soknk', 'soko1', 'sokoL', 'sokok', 'sokoo', 'sokos', 'son:o',
# 'sonk1',
'soLko',
 'soo1o', 'sooL1', 'sooLk', 'sooLo', 'soofL', 'sookc', 'soos', 'sos', 'sovo1', 'sovok', 'sovoo', 'sovos', 'sovov', 'vok1,']
)
    def type_string(self, s, pmap, tname, delim=None):
        tokens = self.lex.tokenize(s, delim)
        tokens = self.lex.syntax(tokens)
        tokens = self.constant_folding2(tokens)
        (sqli, fullpat, pat, reason) =  self.patmatch(tokens, pmap)

        if not sqli:
            #print 'False: %s %s in %s on full %s' % (tname, reason, pat, fullpat)
            return None
        else:
            #print 'False: %s matched' % (tname)
            pass

        return tname, pat, fullpat, tokens

    def test(self, s):
        m = self.type_string(s, self.pmap_new, 'type1')
        if m:
            return m

        m = self.type_string(s, self.pmap_new, 'type2', "'")
        if m:
            return m

        m = self.type_string(s, self.pmap_new, 'type3', '"')
        if m:
            return m

        return None

    def normalize(self, s):
        while True:
            snew = unquote(s)
            if s == snew:
                break
            s = snew.upper()

        # common html cut-n-paste problem
        # we do NOT want to make this a '"'
        # since they one could attack by inserting &QUOT; which
        # SQL will know, but we'll think it's a "
        s = s.replace('&QUOT;', '"')

        s = s.replace('&#39;', '\'')
        return s

    # simplfies  basic arithmetic expressions tha might be used
    # as english abbreviatio
    # merges ';;' in to ';'
    def constant_folding2(self, tokens):
        tlen = len(tokens)
        if tlen == 0:
            return tokens

         # skip all leading left-parens and unary chars
        index = 0
        while index < tlen:
            if tokens[index][0] == 'L':
                index += 1
            elif tokens[index][0] == 'o' and tokens[index][1] in ('-', '+', '~'):
                index +=1
            else:
                break


        newt = []


        last = None
        isunary = False
        for t in tokens[index:]:

            if len(newt) == 5:
                if last and last[0] == 'o':
                    newt.append( last )
                newt += tokens[index:]
                return newt

            index += 1


            # skip over repeated runs of unary operators
            # 1+---+2 -> 1+2 -> 1
            if t[0] == 'o' and t[1] in ('!', '+', '-', '~'):
                if isunary:
                    continue
                else:
                    isunary = True
            else:
                isunary = False

            if t[0] == '1':
                if last == None or last[0] == '1' or last[0]==';':
                    newt.append(t)
                    last = t
                else:
                    last = t
            elif t[0] == 'x':
                if last == None or last[0] in ('n', ';', '1'):
                    newt.append(t)
                    last = t
                else:
                    last = t
            elif t[0] == 'X':
                if last == None or last[0] in ('n', ';', '1'):
                    newt.append(t)
                    last = t
                else:
                    last = t
            elif t[0] == 'o' and t[1] in ('!', '+', '-', '~', '/', '%', '*', 'MOD', 'DIV'):
                #print 'current is operator: ' + t[1]
                if last and last[0] == '1':
                    #print 'and last is number'
                    last = t
                elif last and last[0] == 'n':
                    #print 'and last is number'
                    last = t
                elif last and last[0] == 'o' and last[1] in ('!', '+', '-', '~', '/', '%', '*', 'MOD', 'DIV'):
                    pass
                else:
                    newt.append(t)
                    last = None
            elif t[0] == ';':
                if last and last[0] == ';':
                    pass
                elif last and last[0] == 'o':
                    newt.append( last )
                    last = t
                else:
                    newt.append( t )
                    last = t
            else:
                if last and last[0] == 'o':
                    newt.append( last )
                newt.append(t)
                last = None

        if last and last[0] == 'o':
            newt.append( last )
        return newt

    def is_valid_sql(self, pat, tokens=None):
        tlen = len(tokens)
        # common english screwups

        if tlen == 5:
            if pat in ('so1on', 'no1oo', 'no1of'):
                return 'too short'
            elif pat in ('no1o1', '1ono1'):
                if tokens[1][1] in ('AND', 'OR', '&&', '||') and tokens[1][1] != tokens[3][1]:
                    return None
                else:
                    return 'bogon'

        pat5 = pat[0:5]
        if pat5 in ('sonos', 'sono1', 'sosos', '1ono1', 'so1on', 'sonoo', 'no1oL', 'no1o1'):
            if tlen == 5 and tokens[1][1] != tokens[3][1] and tokens[1][1] not in ('&',):
                return None
            elif tokens[1][1] in ('UNION', 'UNION ALL'):
                return None
            elif tokens[1][1] in ('AND', 'OR', '&&', '||') and tokens[1][1] != tokens[3][1]:
                return None
            #elif tokens[3][1] in ('AND', 'OR', '&&', '||') and tokens[1][1] != tokens[3][1]:
            #    return None
            else:
                return "Unlikely"
        elif pat5.endswith('f') and tlen > 5 and pat[5] != 'L':
            return 'function missing left'



        if tlen <= 4:
            if pat == 'sos':
                if tokens[1][1] in ('*', '/', '-', '+'):
                    return 'too small, harmless'

                isnormal_left = tokens[0][1][0] in ('"',"'")
                isnormal_right = tokens[2][1][-1] in ('"',"'")
                isempty_right = len(tokens[2][1]) == 1
                isenglish = tokens[1][1] in ('AND','&','NOT','UNION','IS','MOD')
                if isenglish:
                    # open string  ...foo "LIKE"
                    return "pat is string-operator-string and operator is logical"
                elif isnormal_left and isnormal_right:
                    # "FOO" + "BAR", type1 style
                    return "fully formed type1 sos -- ignoring"
                elif not isnormal_left and isempty_right:
                    return "not much of an attack"
                elif isnormal_left and not isnormal_right:
                    return "looks like truncation"
            elif pat == 'soos':
                if tokens[1][1] == tokens[2][1]:
                    return "likely double typing or AND or OR"

            elif pat == 'sc':
                if self.alpha_str_re.match(tokens[0][1]):
                    return None
                else:
                    return "gibberish"

            elif (pat in ('sk1','1k1')):
                if (tokens[1][1] not in ('ORDER BY', 'GROUP BY', 'OWN3D BY')):
                    return "pat is string-k-number but k not order/group by"

            elif pat == '1ok':
                # sqli fragment
                if tokens[1][1] not in ( 'UNION', 'UNION ALL'):
                    return 'too short'

            # right start, but too short to sqli
            elif pat in ('n;kn', 'no1o'):
                return "too short"

        return None

    def patmatch(self, tokens, pmap):
        fullpat = ''.join([ t[0] for t in tokens ])
        pat = fullpat[0:5]
        if pat in pmap:
            oksql =self.is_valid_sql(fullpat, tokens)
            if oksql is None:
                return (True, fullpat, pat, '')
            else:
                return (False, fullpat, pat, oksql)
        return (False, fullpat, '', 'No starting pattern found')


import logging
from time import time

def byline(fd, outfd):
    import urlparse
    import time
    parse_qsl = urlparse.parse_qsl
    at = Attacker()

    tstart = time.time()
    t0= time.time()
    imax = 1000000
    count = 0
    alpha_match = at.alpha_re.match
    for line in fd:
        #print line
        count += 1
        if count % imax  == 0:
            t1 = time.time()
            logging.debug("%d, Lap TPS: %d, Lap: %f, Elapsed TPS: %d, Elapsed: %f" % (count, int(imax/(t1-t0)), t1-t0, int(count/(t1 - tstart)), (t1-tstart)))
            t0= time.time()

        #pos = line.find('?')
        #if pos == -1:
        #    continue
        #qs = line[pos+1:-1]
        qs = line.strip()

        if False:
            a1 = at.normalize(unquote(qs).upper())
            attack = at.test(a1)
            if attack is not None:
                a1 = a1.replace("\n", "\\n")
                outfd.write("%s\t%s\t%s\n" % (attack[0],attack[1],a1,))
                outfd.flush()
            else:
                #print "failed: " + a1
                pass

        else:
            for (key, value) in parse_qsl(qs):
                if alpha_match(value):
                    continue
                # note: value is already unquoted
                #a1 = at.normalize(unquote_plus(value).upper())
                a1 = at.normalize(value.upper())
                attack = at.test(a1)
                if attack is not None:
                    a1 = a1.replace("\n", "\\n")
                    outfd.write("%s\t%s\t%s\n" % (attack[0],attack[1],a1,))
                    outfd.flush()

    t1= time.time()
    logging.debug("%d, Elapsed TPS: %d, Elapsed: %f" % (count, int(count/(t1 - tstart)), (t1-tstart)))

import sys

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fd = sys.stdin
    outfd = sys.stdout
    byline(fd, outfd)
