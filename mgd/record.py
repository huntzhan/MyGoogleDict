from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime
import xml.etree.ElementTree as ET

from google_translate_api import TranslateService

from mgd.share import (
    decorate_all_methods,
    debug_return_val,
    ensure_decode,
)
from mgd.data_io import RecordIO

try:
    str = unicode
except:
    pass


_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
_ROOT = 'root'
_RECORD = 'record'
_FROM_LANG = 'from_lang'
_TO_LANG = 'to_lang'
_DATA = 'data'
_RESULT = 'result'
_SENTENCE = 'sentence'
_DICT = 'dict'
_POS = 'pos'
_MEANING = 'meaning'
_TIME = 'time'


@decorate_all_methods(debug_return_val)
class Record:

    def __init__(self, debug=False):
        self._debug = debug
        self._record_io = RecordIO()

    def _load_xml(self, field_name):
        try:
            # WTF? fromstring only accept bytes?
            xml_content = getattr(self._record_io, field_name)
            xml = ET.fromstring(xml_content)
        except:
            # "The element name, attribute names, and attribute values can be
            # either bytestrings or Unicode strings." Thus, unicode should be
            # ok.
            xml = ET.Element(_ROOT)
        return xml

    def _write_xml(self, xml, field_name):
        # Holly Shit, ASCII encoding works.
        raw_xml = ET.tostring(xml)
        setattr(self._record_io, field_name, raw_xml)

    def _merge_records_from_cache(self, force_merge=False):
        if not self._record_io.merge_flag and not force_merge:
            return
        # load
        record_xml = self._load_xml('record')
        cache_xml = self._load_xml('cache')

        for node in cache_xml:
            record_xml.append(node)
        cache_xml.clear()

        # write
        self._write_xml(record_xml, 'record')
        self._write_xml(cache_xml, 'cache')

    @ensure_decode
    def add(self,
            from_lang,
            to_lang,
            data,
            result):
        """
        Parameters:
            from_lang: data's language.
            to_lang: result's language.
            data: input text.
            result: translation of data.

            All parameters are decoded to unicode strings if they are whatever
            else.
        Return:
            None.
        """

        has_dict = TranslateService.has_pos_terms_pairs
        extract_pairs = TranslateService.get_pos_terms_pairs_from_json
        extract_sentences = TranslateService.get_senteces_from_json

        # read xml record file
        cache_xml = self._load_xml('cache')

        # "The element name, attribute names, and attribute values can be
        # either bytestrings or Unicode strings." Thus, unicode should be
        # ok.
        new_record = ET.SubElement(cache_xml, _RECORD)

        (from_lang_node, to_lang_node,
         data_node, result_node, time_node) =\
            map(
                # create new elements.
                lambda x: ET.SubElement(new_record, x),
                [
                    _FROM_LANG,
                    _TO_LANG,
                    _DATA,
                    _RESULT,
                    _TIME,
                ],
            )

        # assign unicode strings.
        from_lang_node.text = from_lang
        to_lang_node.text = to_lang
        data_node.text = data
        # current time represented in ISO format. Notice that for Py2,
        # isoformat() returns byte, not unicode, thus unicode()(str = unicode)
        # should be used to assure passing the string in right type.
        time_node.text = str(datetime.now().isoformat())

        # construct result node
        sentence_node = ET.SubElement(result_node, _SENTENCE)
        sentence_node.text = extract_sentences(result)

        # multiple explanations
        if has_dict(result):
            dict_node = ET.SubElement(result_node, _DICT)

            pos_vals_pairs = extract_pairs(result)
            for pos, vals in pos_vals_pairs:
                pos_node = ET.SubElement(dict_node, _POS)
                pos_node.text = pos

                for val in vals:
                    meaning_node = ET.SubElement(pos_node, _MEANING)
                    meaning_node.text = val

        # save content to cache
        self._write_xml(cache_xml, 'cache')
        # judge merge
        self._merge_records_from_cache()

    def display(self):
        # merge first
        self._merge_records_from_cache(force_merge=True)

        # targeting on record file
        record_xml = self._load_xml('record')
        records = []
        for record in record_xml:
            extract_data = (
                record.find(_DATA).text,
                record.find(_RESULT).find(_SENTENCE).text,
                record.find(_TIME).text,
            )
            records.append(extract_data)
        sorted_records = sorted(
            records,
            key=lambda x: datetime.strptime(x[-1], _ISO_FORMAT),
        )

        if not sorted_records:
            print("No Record")
        else:
            for data, result, _ in sorted_records:
                line = "[{}][{}]".format(data, result)
                print(line)
