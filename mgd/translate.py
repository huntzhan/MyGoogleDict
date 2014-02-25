from __future__ import unicode_literals
from __future__ import print_function

import os
import subprocess
import tempfile

from google_translate_api import TranslateService, TTSService
from mgd import data_io

from mgd.share import (
    decorate_all_methods,
    debug_return_val,
    ensure_decode,
    convert_dict_to_key_value_pairs,
    assemble_senteces_from_json,
    DICT,
    SENTENCES,
)


@decorate_all_methods(debug_return_val)
class Translator:

    @ensure_decode
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
        if DICT in result:
            lines = []
            pos_vals_pairs = convert_dict_to_key_value_pairs(result)
            for pos, vals in pos_vals_pairs:
                explanation = OUTPUT_FORMAT.format(
                    pos,
                    ', '.join(vals),
                )
                lines.append(explanation)
            print(os.linesep.join(lines))
        else:
            val = assemble_senteces_from_json(result)
            print(OUTPUT_FORMAT.format(SENTENCES, val))


class Speaker:

    @ensure_decode
    def __init__(self, from_lang, data):
        self._from_lang = from_lang
        self._data = data

    def speak(self):
        tts = TTSService()
        mpeg_binary = tts.get_mpeg_binary(self._from_lang, self._data)
        playback_command = data_io.get_playback_command()

        try:
            f = tempfile.NamedTemporaryFile(bufsize=0)
        except:
            f = tempfile.NamedTemporaryFile(buffering=0)

        f.write(mpeg_binary)
        playback_command.append(f.name)
        subprocess.call(playback_command)
        f.close()
