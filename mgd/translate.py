from __future__ import print_function
from __future__ import unicode_literals
import os
import share
from google_translate_api import TranslateService


@share.decorate_all_methods(share.debug_return_val)
class Translator:

    def __init__(self, from_lang, to_lang, data, debug=False):
        self._debug = debug
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._data = data

    def translate(self):
        translator = TranslateService()
        result = translator.trans_details(
            self._from_lang,
            self._to_lang,
            self._data,
        )
        return result

    @staticmethod
    def display_result(result):
        OUTPUT_FORMAT = '[{}] {}'
        dictionary = result.get(share.DICT, None)
        if dictionary:
            lines = []
            for entity in dictionary:
                explanation = OUTPUT_FORMAT.format(
                    entity[share.POS],
                    ', '.join(entity[share.TERMS]),
                )
                lines.append(explanation)
            print(os.linesep.join(lines))
        else:
            val = ''.join(map(
                lambda x: x[share.TRANS],
                result[share.SENTENCES]
            ))
            print(OUTPUT_FORMAT.format(share.SENTENCES, val))
