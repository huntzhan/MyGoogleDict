import goslate


class Translator:

    def __init__(self, from_lang, to_lang, data):
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._data = data

    def translate(self):
        gs = goslate.Goslate()
        result = gs.translate(
            self._data,
            self._to_lang,
            self._from_lang,
        )
        return result
