#!/usr/bin/env python
"""
Usage: mgd [-f <from_lang>] [-t <to_lang>] [-v|--reverse] <data>
       mgd -r|--record
       mgd -h|--help

Options:
    -f <from_lang>  input language [default: en]
    -t <to_lang>    ouput language [default: zh-CN]
    -v --reverse    reverse -f and -t
    -r --record     display search record
"""
from docopt import docopt
from translate import Translator
from record import Record

if __name__ == '__main__':
    arguements = docopt(__doc__)
    record = Record()
    if arguements['<data>']:
        # translation
        from_lang = arguements['-f']
        to_lang = arguements['-t']
        reverse = arguements['--reverse']
        data = arguements['<data>']
        # reverse langs
        from_lang, to_lang = (to_lang, from_lang)\
            if reverse else (from_lang, to_lang)
        # do translation
        translator = Translator(from_lang, to_lang, data)
        result = translator.translate()
        print(result)
        # add record
        record.add(from_lang, to_lang, data, result)

    else:
        # display
        record.display()
