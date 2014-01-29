from __future__ import print_function
from __future__ import unicode_literals
import os
import subprocess
import tempfile
import share
from google_translate_api import TranslateService
from google_translate_api import TTSService
import data_io


@share.decorate_all_methods(share.debug_return_val)
class Translator:

    @share.ensure_decode
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
        if share.DICT in result:
            lines = []
            pos_vals_pairs = share.convert_dict_to_key_value_pairs(result)
            for pos, vals in pos_vals_pairs:
                explanation = OUTPUT_FORMAT.format(
                    pos,
                    ', '.join(vals),
                )
                lines.append(explanation)
            print(os.linesep.join(lines))
        else:
            val = share.assemble_senteces_from_json(result)
            print(OUTPUT_FORMAT.format(share.SENTENCES, val))


class Speaker:

    @share.ensure_decode
    def __init__(self, from_lang, data):
        self._from_lang = from_lang
        self._data = data

    def speak(self):
        tts = TTSService()
        mpeg_binary = tts.get_mpeg_binary(self._from_lang, self._data)
        playback_command = data_io.get_playback_command()

        with tempfile.NamedTemporaryFile(bufsize=0) as f:
            f.write(mpeg_binary)
            playback_command.append(f.name)
            subprocess.call(playback_command)
