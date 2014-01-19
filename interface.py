#!/usr/bin/env python
"""
Usage: mgd [--debug] [-f <from_lang>] [-t <to_lang>] [-v|--reverse] <data>...
       mgd [--debug] -r|--record
       mgd -h|--help

Options:
    -f <from_lang>  input language [default: en]
    -t <to_lang>    ouput language [default: zh-CN]
    -v --reverse    reverse -f and -t
    -r --record     display search record
    --debug         display runtime information
"""
from docopt import docopt
from translate import Translator
from record import Record


def _assemble_data(raw_data):
    # raw_data should be a list, according to docopt's document.
    assert type(raw_data) is list

    if len(raw_data) == 1:
        # single word
        return raw_data[0]
    elif len(raw_data) > 1:
        # multi-word sentence.
        return ' '.join(raw_data)


def _extract(arguements):
    from_lang = arguements['-f']
    to_lang = arguements['-t']
    data = _assemble_data(arguements['<data>'])
    reverse = arguements['--reverse']
    # reverse langs
    from_lang, to_lang = (to_lang, from_lang)\
        if reverse else (from_lang, to_lang)

    return from_lang, to_lang, data


if __name__ == '__main__':
    arguements = docopt(__doc__, version='0.1')

    record = Record(debug=arguements['--debug'])
    if arguements['<data>']:
        # translation
        from_lang, to_lang, data = _extract(arguements)

        # translate data
        translator = Translator(from_lang, to_lang, data,
                                debug=arguements['--debug'])
        # result is a dictionary contains decoded infomation of the
        # trnaslation.
        result = translator.translate()
        translator.display_result(result)
        # add record
        record.add(from_lang, to_lang,
                   data, result)

    elif arguements['--record']:
        # display record
        record.display()
    else:
        raise Exception('No Implemented Yet.')
