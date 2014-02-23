from __future__ import print_function

from datetime import datetime
import xml.etree.ElementTree as ET

from mgd import share
from mgd.data_io import RecordIO


_UTF8 = 'UTF-8'
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


@share.decorate_all_methods(share.debug_return_val)
class Record:

    def __init__(self, debug=False):
        self._debug = debug
        self._record_io = RecordIO()

    def _load_xml(self, field_name):
        try:
            xml_content = getattr(self._record_io, field_name)
            xml = ET.fromstring(xml_content)
        except:
            # new one
            xml = ET.Element(_ROOT)
        return xml

    def _write_xml(self, xml, field_name):
        raw_xml = ET.tostring(xml, encoding=_UTF8)
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

    @share.ensure_decode
    def add(self,
            from_lang,
            to_lang,
            data,
            result):

        # read xml record file
        cache_xml = self._load_xml('cache')

        new_record = ET.SubElement(cache_xml, _RECORD)

        # sub nodes
        from_lang_node = ET.SubElement(new_record, _FROM_LANG)
        to_lang_node = ET.SubElement(new_record, _TO_LANG)
        data_node = ET.SubElement(new_record, _DATA)
        result_node = ET.SubElement(new_record, _RESULT)
        time_node = ET.SubElement(new_record, _TIME)

        # assign values
        from_lang_node.text = from_lang
        to_lang_node.text = to_lang

        # make sure input source is decoded
        data_node.text = data
        time_node.text = datetime.now().isoformat()

        # construct result node
        sentence_node = ET.SubElement(result_node, _SENTENCE)
        sentence_node.text = share.assemble_senteces_from_json(result)

        # multiple explanations
        if share.DICT in result:
            dict_node = ET.SubElement(result_node, _DICT)

            pos_vals_pairs = share.convert_dict_to_key_value_pairs(result)
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
