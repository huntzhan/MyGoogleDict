from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime
import xml.etree.ElementTree as ET

from mgd.share import (decorate_all_methods,
                       debug_return_val,
                       ensure_decode,
                       assemble_senteces_from_json,
                       convert_dict_to_key_value_pairs,
                       DICT,)
from mgd.data_io import RecordIO

try:
    unicode
except:
    str = unicode


class _GLOBAL:
    UTF8 = 'UTF-8'
    ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
    ROOT = 'root'
    RECORD = 'record'
    FROM_LANG = 'from_lang'
    TO_LANG = 'to_lang'
    DATA = 'data'
    RESULT = 'result'
    SENTENCE = 'sentence'
    DICT = 'dict'
    POS = 'pos'
    MEANING = 'meaning'
    TIME = 'time'


@decorate_all_methods(debug_return_val)
class Record:

    def __init__(self, debug=False):
        self._debug = debug
        self._record_io = RecordIO()

    def _load_xml(self, field_name):
        try:
            xml_content = getattr(self._record_io, field_name)
            # Since fromstring() only accept string, xml_content, which is
            # stored in bytes, must be decode.
            xml = ET.fromstring(xml_content.decode(_GLOBAL.UTF8))
        except:
            # "The element name, attribute names, and attribute values can be
            # either bytestrings or Unicode strings." Thus, unicode should be
            # ok.
            xml = ET.Element(_GLOBAL.ROOT)
        return xml

    def _write_xml(self, xml, field_name):
        # raw_xml is the string representation of an XML element, encoded in
        # UTF-8 and stored in bytes.
        raw_xml = ET.tostring(xml, encoding=_GLOBAL.UTF8)
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

        # read xml record file
        cache_xml = self._load_xml('cache')

        # "The element name, attribute names, and attribute values can be
        # either bytestrings or Unicode strings." Thus, unicode should be
        # ok.
        new_record = ET.SubElement(cache_xml, _GLOBAL.RECORD)

        (from_lang_node, to_lang_node,
         data_node, result_node, time_node) =\
            map(
                # create new elements.
                lambda x: ET.SubElement(new_record, x),
                [
                    _GLOBAL.FROM_LANG,
                    _GLOBAL.TO_LANG,
                    _GLOBAL.DATA,
                    _GLOBAL.RESULT,
                    _GLOBAL.TIME,
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
        sentence_node = ET.SubElement(result_node, _GLOBAL.SENTENCE)
        sentence_node.text = assemble_senteces_from_json(result)

        # multiple explanations
        if DICT in result:
            dict_node = ET.SubElement(result_node, _GLOBAL.DICT)

            pos_vals_pairs = convert_dict_to_key_value_pairs(result)
            for pos, vals in pos_vals_pairs:
                pos_node = ET.SubElement(dict_node, _GLOBAL.POS)
                pos_node.text = pos

                for val in vals:
                    meaning_node = ET.SubElement(pos_node, _GLOBAL.MEANING)
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
                record.find(_GLOBAL.DATA).text,
                record.find(_GLOBAL.RESULT).find(_GLOBAL.SENTENCE).text,
                record.find(_GLOBAL.TIME).text,
            )
            records.append(extract_data)
        sorted_records = sorted(
            records,
            key=lambda x: datetime.strptime(x[-1], _GLOBAL.ISO_FORMAT),
        )

        if not sorted_records:
            print("No Record")
        else:
            for data, result, _ in sorted_records:
                line = "[{}][{}]".format(data, result)
                print(line)
