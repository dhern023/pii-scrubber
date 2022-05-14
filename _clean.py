"""
Normalize text by cleaning strings
"""

import re

regex_formatting = r'\r|\t|\n|\f|\v'
regex_spacings = r'\s\s+'

def clean_string(string, regex, replacement = ''):
    string_p = (
        re.sub(regex, replacement, string)
        .strip()
    )
    return string_p