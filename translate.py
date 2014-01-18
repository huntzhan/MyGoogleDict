from __future__ import print_function
from __future__ import unicode_literals
import os
from goslate import AdjustedGoslate


class Translator:

    def __init__(self, from_lang, to_lang, data):
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._data = data

    def translate(self):
        gs = AdjustedGoslate()
        result = gs.translate(
            self._data,
            self._to_lang,
            self._from_lang,
        )
        return result

    @staticmethod
    def display_result(result):
        OUTPUT_FORMAT = '[{}] {}'
        dictionary = result.get(AdjustedGoslate.DICT, None)
        if dictionary:
            lines = []
            for pos, vals in dictionary.items():
                explanation = OUTPUT_FORMAT.format(
                    pos,
                    ', '.join(vals),
                )
                lines.append(explanation)
            print(os.linesep.join(lines))
        else:
            val = result[AdjustedGoslate.SENTENCE]
            print(OUTPUT_FORMAT.format(
                AdjustedGoslate.SENTENCE, val))
