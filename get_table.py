#!/usr/bin/python3

import re
import os
import sys
from common import *

String = '''
RegExr was created by gskinner.com, and is proudly hosted by Media Temple.

Edit the Expression & Text to see matches. Roll over matches or the expression for details. PCRE & Javascript flavors of RegEx are supported.

The side bar includes a Cheatsheet, full Reference, and Help. You can also Save & Share with the Community, and view patterns you create or your favorite in My Patterns.

REgexr
Explore results with the Tools below. Replace & List output custom results. Details lists capture groups. Explain describes your expression in plain English.



'''

wordPat = Partten('^R[eE]g[eE]xr|English.$|you[r]?')

if wordPat.is_found(String):
    
    printError(wordPat.findall(String))
