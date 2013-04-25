#
# ALPHA
# libinjection module for python
#
#  Copyright 2012, 2013 Nick Galbreath
#  nickg@client9.com
#  BSD License -- see COPYING.txt for details
#
#

from distutils.core import setup, Extension

module1 = Extension('libinjection',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = ['/usr/local/include'],
                    libraries = [],
                    library_dirs = [],
                    sources = ['libinjection_module.c', 'sqlparse.c']
                    )

setup (name = 'libinjection',
       version = '1.0',
       description = 'Wrapper around libinjection c-code to detect sqli',
       author = 'Nick Galbreath',
       author_email = 'nickg@client9.com',
       url = 'http://client9.com/libinjection',
       long_description = '''
wrapper around libinjection
''',
       ext_modules = [module1])
