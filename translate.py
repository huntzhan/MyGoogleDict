from __future__ import print_function
from __future__ import unicode_literals
import os
from share import debug_return_val
from share import decorate_all_methods
from goslate import AdjustedGoslate


@decorate_all_methods(debug_return_val)
class Translator:

    def __init__(self, from_lang, to_lang, data, debug=False):
        self._debug = debug
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._data = data

    def translate(self):
        _RECONNECT_TIMES = 5
        reconnect_times = _RECONNECT_TIMES

        gs = AdjustedGoslate(debug=self._debug)
        result = None
        while reconnect_times > 0:
            try:
                result = gs.translate(
                    self._data,
                    self._to_lang,
                    self._from_lang,
                )
                # quit
                reconnect_times = 0
            except:
                reconnect_times -= 1

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
            print(OUTPUT_FORMAT.format(AdjustedGoslate.SENTENCE, val))
