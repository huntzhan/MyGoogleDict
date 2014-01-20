from __future__ import print_function
from __future__ import unicode_literals

import json

from goslate import Goslate
from goslate import Error

try:
    from urllib.request import build_opener, Request, HTTPHandler, HTTPSHandler
    from urllib.parse import quote_plus, urlencode, unquote_plus
except ImportError:
    from urllib2 import build_opener, Request, HTTPHandler, HTTPSHandler
    from urllib import urlencode, unquote_plus, quote_plus


try:
    unicode
except NameError:
    unicode = str


class AdjustedGoslate(Goslate):
    DICT = u'dict'
    SENTENCE = u'sentence'

    def translate(self, text, target_language, source_language=''):

        if not target_language:
            raise Error('invalid target language')

        if not text.strip():
            return u'', unicode(target_language)

        GOOGLE_TRASLATE_URL = 'http://translate.google.com/translate_a/t'
        GOOGLE_TRASLATE_PARAMETERS = {
            'client': 'z',
            'sl': source_language,
            'tl': target_language,
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'text': text
        }

        url = '?'.join(
            (GOOGLE_TRASLATE_URL, urlencode(GOOGLE_TRASLATE_PARAMETERS))
        )
        response_content = self._open_url(url)
        # That's what I want.
        data = json.loads(response_content)

        # extract sentence for multiple words translation
        sentence = u''.join(i['trans'] for i in data['sentences'])
        # extract the result of single word translation
        dictionary = data.get(u'dict', None)

        meanings = {}
        meanings[self.SENTENCE] = sentence
        if dictionary:
            meanings[self.DICT] = {}
            for item in dictionary:
                meanings[self.DICT][item[u'pos']] = item[u'terms']
        return meanings
