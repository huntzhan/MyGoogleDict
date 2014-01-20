#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''Unit test for goslate module
'''

from __future__ import unicode_literals
import sys
import os
import unittest
import doctest        
import goslate
import types
import itertools
import io

from goslate import *
from goslate import _main

__author__ = 'ZHUO Qiang'
__date__ = '2013-05-14'

gs = Goslate()

class UnitTest(unittest.TestCase):
    if sys.version < '3':
        pass
    else:
        assertRaisesRegexp = unittest.TestCase.assertRaisesRegex
    
    def assertIsGenerator(self, generator):
        if not isinstance(generator, types.GeneratorType) and not isinstance(generator, itertools.chain):
            raise self.failureException('type is not generator: %s, %s' % (type(generator), generator))
        
    
    def assertGeneratorEqual(self, expectedResult, generator):
        self.assertIsGenerator(generator)
        self.assertListEqual(list(expectedResult), list(generator))
        
        
    def test__basic_translate(self):
        self.assertEqual((u'', u'en'), gs._basic_translate(b'\n \t\n', 'en'))
        
        self.assertEqual((u'hello world.', u'en'), gs._basic_translate(b'hello world.', 'en'))
        self.assertEqual((u'你好世界。', u'en'), gs._basic_translate(b'hello world.', 'zh-cn'))
        self.assertEqual((u'你好世界。', u'de'), gs._basic_translate(b'hallo welt. \n\n', 'zh-CN'))
        self.assertNotEqual(u'你好世界。', gs._basic_translate(b'hallo welt.', 'zh-CN', 'en')[0])
        self.assertEqual((u'你好世界。\n\n你好', u'en'), gs._basic_translate(b'\n\nhello world.\n\nhello\n\n', 'zh-cn'))

        test_string = b'hello     '
        max_allowed_times = int(gs._MAX_LENGTH_PER_QUERY / len(test_string) - 1)
        self.assertEqual((u'你好'*max_allowed_times, u'en'), gs._basic_translate(test_string*max_allowed_times, 'zh'))
        self.assertRaisesRegexp(Error, 'input too large', gs._basic_translate, test_string*(max_allowed_times+10), 'zh')
        self.assertRaisesRegexp(Error, 'invalid target language', gs._basic_translate, b'hello', '')
        
        
    def test_translate(self):
        self.assertEqual(u'', gs.translate(b'\n \n\t\n', 'en'))
        
        self.assertEqual(u'你好世界。', gs.translate(b'hello world.', 'zh'))
        self.assertEqual(u'Hello World.', gs.translate(u'你好世界。', 'en', 'zh'))
        self.assertEqual(u'Hello World.', gs.translate(u'你好世界。'.encode('utf-8'), 'en'))
        self.assertEqual(u'你好世界。', gs.translate(b'hello world.', 'zh-cn', u'en'))
        self.assertEqual(u'你好世界。', gs.translate(b'hallo welt.', u'zh-CN'))
        self.assertEqual(u'你好世界。', gs.translate(u'hallo welt.', 'zh-CN', 'de'))
        
        self.assertRaisesRegexp(Error, 'invalid target language', gs.translate, '', '')
        
        self.assertNotEqual(u'你好世界。', gs.translate(b'hallo welt.', u'zh-CN', 'en'))

        test_string = b'helloworld'
        exceed_allowed_times = int(gs._MAX_LENGTH_PER_QUERY / len(test_string) + 10)
        self.assertRaisesRegexp(Error, 'input too large', gs.translate, test_string*exceed_allowed_times, 'zh')

        self.assertRaisesRegexp(Error, 'invalid target language', gs.translate, 'hello', '')
        
        self.assertEqual(u'你好世界。\n\n你好', gs.translate(u'\n\nhello world.\n\nhello\n\n', 'zh-cn'))

        test_string = u'hello!    '
        exceed_allowed_times = int(gs._MAX_LENGTH_PER_QUERY / len(test_string) + 10)
        self.assertEqual(u'你好！'*exceed_allowed_times, gs.translate(test_string*exceed_allowed_times, 'zh'))
        

    def test_translate_batch_input(self):
        self.assertGeneratorEqual([], gs.translate((), 'en'))        
        self.assertGeneratorEqual([u''], gs.translate([b'\n \n\t\n'], 'en'))
        self.assertGeneratorEqual([u'你好世界。'], gs.translate([u'hello world.'], 'zh-cn'))
        self.assertGeneratorEqual([u'你好世界。'], gs.translate([b'hello world.'], 'zh-CN', u'en'))
        self.assertGeneratorEqual([u'你好世界。'], gs.translate([b'hallo welt.'], u'zh-CN'))
        self.assertGeneratorEqual([u'你好世界。\n\n你好'], gs.translate([b'\n\nhello world.\n\nhello\n\n'], 'zh-cn'))
        self.assertNotEqual([u'你好世界。'], gs.translate([b'hallo welt.'], 'zh-CN', 'en'))
        self.assertRaisesRegexp(Error, 'invalid target language', gs.translate, [''], u'')
        
        test_string = b'helloworld'
        exceed_allowed_times = int(gs._MAX_LENGTH_PER_QUERY / len(test_string) + 1)
        self.assertRaisesRegexp(Error, 'input too large', list, gs.translate((u'a', test_string*exceed_allowed_times), 'zh'))


        test_string = b'hello!    '
        exceed_allowed_times = int(gs._MAX_LENGTH_PER_QUERY / len(test_string) + 10)
        self.assertGeneratorEqual([u'你好！'*exceed_allowed_times]*3, gs.translate((test_string*exceed_allowed_times,)*3, 'zh'))
        self.assertGeneratorEqual([u'你好世界。', u'你好'], gs.translate([b'\n\nhello world.\n', b'\nhello\n\n'], 'zh-cn'))
        

    def test_translate_batch_input_with_empty_string(self):
        self.assertGeneratorEqual([u'你好世界。', u''], gs.translate([u'hello world.', u''], 'zh-cn'))
        self.assertGeneratorEqual([u'你好世界。', u'', u'你好'], gs.translate([u'hello world.', u'', u'hello'], 'zh-cn'))
        self.assertGeneratorEqual([u'', u'你好世界。'], gs.translate([u'', u'hello world.'], 'zh-cn'))        
        
        
    def test_detect(self):
        self.assertEqual('en', gs.detect(b''))
        self.assertEqual('en', gs.detect(b'\n\r  \n'))
        self.assertEqual('en', gs.detect(b'hello world'))
        self.assertEqual('zh-CN', gs.detect(u'你好世界'.encode('utf-8')))
        self.assertEqual('de', gs.detect(u'hallo welt.'))
        
        self.assertEqual('zh-CN', gs.detect(u'你好世界'.encode('utf-8')*1000))
        
    def test_detect_batch_input(self):
        self.assertGeneratorEqual(['en', 'zh-CN', 'de', 'en']*10,
                                  gs.detect((u'hello world', u'你好世界'.encode('utf-8'), u'hallo welt.', '')*10))

        self.assertGeneratorEqual(['en', 'zh-CN', 'de', 'en']*10,
                                  gs.detect([b'hello world'*10, u'你好世界'*100, b'hallo welt.'*1000, u'\n\r \t'*1000]*10))


    def test_translate_massive_input(self):
        times = 1000
        source = (u'hello world. %s' % i for i in range(times))
        result = gs.translate((i.encode('utf-8') for i in source), 'zh-cn')
        self.assertGeneratorEqual((u'你好世界。 %s' % i for i in range(times)), result)

        
    def test_main(self):
        encoding = sys.getfilesystemencoding()
        # sys.stdout = StringIO()
        
        sys.stdout = io.BytesIO()
        sys.stdin = io.BytesIO(b'hello world')
        _main([sys.argv[0], '-t', 'zh-CN'])
        self.assertEqual(u'你好世界\n'.encode(encoding), sys.stdout.getvalue())
        
        sys.stdout = io.BytesIO()
        sys.stdin = io.BytesIO(u'你好'.encode(encoding))
        _main([sys.argv[0], '-t', 'en'])
        self.assertEqual(u'Hello\n'.encode(encoding), sys.stdout.getvalue())
        
        sys.stdout = io.BytesIO()
        sys.stdin = io.BytesIO(b'hello world')
        _main([sys.argv[0], '-t', 'zh-CN', '-o', 'utf-8'])
        self.assertEqual(u'你好世界\n'.encode('utf-8'), sys.stdout.getvalue())
        
        sys.stdout = io.BytesIO()        
        sys.stdin = io.BytesIO(u'你好'.encode('utf-8'))
        _main([sys.argv[0], '-t', 'en', '-i', 'utf-8'])
        self.assertEqual(u'Hello\n'.encode(encoding), sys.stdout.getvalue())
        
        sys.stdout = io.BytesIO()        
        with open('for_test.tmp', 'w') as f:
            f.write('hello world')
        _main([sys.argv[0], '-t', 'zh-CN', f.name])
        self.assertEqual(u'你好世界\n'.encode(encoding), sys.stdout.getvalue())
        
        sys.stdout = io.BytesIO()        
        with open('for_test.tmp', 'w') as f:
            f.write('hello world')
        _main([sys.argv[0], '-t', 'zh-CN', '-o', 'utf-8', f.name])
        self.assertEqual(u'你好世界\n'.encode('utf-8'), sys.stdout.getvalue())
        
        sys.stdout = io.BytesIO()
        with io.open('for_test.tmp', 'w', encoding=encoding) as f:
            f.write(u'你好')
        _main([sys.argv[0], '-t', 'en', f.name])
        self.assertEqual(u'Hello\n'.encode(encoding), sys.stdout.getvalue())
        
        sys.stdout = io.BytesIO()
        with io.open('for_test.tmp', 'w', encoding='utf-8') as f:
            f.write(u'你好')
        _main([sys.argv[0], '-t', 'en', '-i', 'utf-8', f.name])
        self.assertEqual(u'Hello\n'.encode(encoding), sys.stdout.getvalue())

        sys.stdout = io.BytesIO()        
        with io.open('for_test.tmp', 'w', encoding='utf-8') as f:
            f.write(u'你好')
        with io.open('for_test_2.tmp', 'w', encoding='utf-8') as f2:
            f2.write(u'世界')
            
        _main([sys.argv[0], '-t', 'en', '-i', 'utf-8', f.name, f2.name])
        self.assertEqual(u'Hello\nWorld\n'.encode(encoding), sys.stdout.getvalue())
        

    def test_get_languages(self):
        expected = {
            'el': 'Greek',
            'eo': 'Esperanto',
            'en': 'English',
            'zh': 'Chinese',
            'af': 'Afrikaans',
            'sw': 'Swahili',
            'ca': 'Catalan',
            'it': 'Italian',
            'iw': 'Hebrew',
            'cy': 'Welsh',
            'ar': 'Arabic',
            'ga': 'Irish',
            'cs': 'Czech',
            'et': 'Estonian',
            'gl': 'Galician',
            'id': 'Indonesian',
            'es': 'Spanish',
            'ru': 'Russian',
            'nl': 'Dutch',
            'pt': 'Portuguese',
            'mt': 'Maltese',
            'tr': 'Turkish',
            'lt': 'Lithuanian',
            'lv': 'Latvian',
            'tl': 'Filipino',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'ro': 'Romanian',
            'is': 'Icelandic',
            'pl': 'Polish',
            'yi': 'Yiddish',
            'be': 'Belarusian',
            'fr': 'French',
            'bg': 'Bulgarian',
            'uk': 'Ukrainian',
            'sl': 'Slovenian',
            'hr': 'Croatian',
            'de': 'German',
            'ht': 'Haitian Creole',
            'da': 'Danish',
            'fa': 'Persian',
            'hi': 'Hindi',
            'fi': 'Finnish',
            'hu': 'Hungarian',
            'ja': 'Japanese',
            'zh-TW': 'Chinese (Traditional)',
            'sq': 'Albanian',
            'no': 'Norwegian',
            'ko': 'Korean',
            'sv': 'Swedish',
            'mk': 'Macedonian',
            'sk': 'Slovak',
            'zh-CN': 'Chinese (Simplified)',
            'ms': 'Malay',
            'sr': 'Serbian',}
        self.assertDictEqual(expected, gs.get_languages())
        
        
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(goslate))
    return tests        
        

if __name__ == '__main__':
    unittest.main()
