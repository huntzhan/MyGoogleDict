from __future__ import print_function
import os
import gzip
import inspect
from datetime import datetime
import pickle
import xml.etree.ElementTree as ET
from functools import wraps
from goslate import AdjustedGoslate


_UTF8 = 'UTF-8'
_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def _ensure_decode(func):
    def utf8_decoder(text):
        try:
            decoded = text.decode(_UTF8)
        except:
            # both decoded text and result(a dictionary variable contains
            # decoded information) would trigger exception. In this case, just
            # return the argument.
            decoded = text
        return decoded

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        decoded_args = map(utf8_decoder, args)
        decoded_kwargs = {k: utf8_decoder(v) for k, v in kwargs.items()}
        return func(self, *decoded_args, **decoded_kwargs)
    return wrapper


class Record:
    # FILE_NAME = 'search_record.xml.gz'
    FILE_NAME = 'search_record.pickle.gz'
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

    def __init__(self):
        # get path of search record
        self._dir_path = self._get_dir_path()
        self._file_path = os.path.join(
            self._dir_path,
            Record.FILE_NAME,
        )

    def _get_dir_path(self):
        dir = inspect.getmodule(self)
        path = dir.__file__
        dir_path, _ = os.path.split(path)
        return dir_path

    def _load_xml(self, xml_path):
        try:
            with gzip.open(xml_path) as f:
                xml_content = f.read()
            xml = ET.fromstring(xml_content)
        except:
            # new one
            xml = ET.Element(Record.ROOT)
        return xml

    def _write_xml(self, xml):
        raw_xml = ET.tostring(xml, encoding=_UTF8)
        with gzip.open(self._file_path, 'wb') as f:
            f.write(raw_xml)

    def _pickle_load_xml(self, xml_path):
        try:
            with gzip.open(xml_path) as f:
                xml = pickle.load(f)
        except:
            # new one
            xml = ET.Element(Record.ROOT)
        return xml

    def _pickle_write_xml(self, xml):
        with gzip.open(self._file_path, 'wb') as f:
            pickle.dump(xml, f)

    @_ensure_decode
    def add(self,
            from_lang,
            to_lang,
            data,
            result):

        # read xml record file
        record_xml = self._pickle_load_xml(self._file_path)

        new_record = ET.SubElement(record_xml, Record.RECORD)

        # sub nodes
        from_lang_node = ET.SubElement(new_record, Record.FROM_LANG)
        to_lang_node = ET.SubElement(new_record, Record.TO_LANG)
        data_node = ET.SubElement(new_record, Record.DATA)
        result_node = ET.SubElement(new_record, Record.RESULT)
        time_node = ET.SubElement(new_record, Record.TIME)

        # assign values
        from_lang_node.text = from_lang
        to_lang_node.text = to_lang

        # make sure input source is decoded
        data_node.text = data
        time_node.text = datetime.now().isoformat()

        # construct result node
        sentence_node = ET.SubElement(result_node, Record.SENTENCE)
        sentence_node.text = result[AdjustedGoslate.SENTENCE]

        # multiple explanations
        if AdjustedGoslate.DICT in result:
            dict_node = ET.SubElement(result_node, Record.DICT)
            for pos, vals in result.get(AdjustedGoslate.DICT).items():
                pos_node = ET.SubElement(dict_node, Record.POS)
                # pos could be empty, I don't know why.
                pos_node.text = pos or 'error_pos'

                for val in vals:
                    meaning_node = ET.SubElement(pos_node, Record.MEANING)
                    meaning_node.text = val

        # save content
        self._pickle_write_xml(record_xml)

    def display(self):
        record_xml = self._pickle_load_xml(self._file_path)
        records = []
        for record in record_xml:
            extract_data = (
                record.find(Record.DATA).text,
                record.find(Record.RESULT).find(Record.SENTENCE).text,
                record.find(Record.TIME).text,
            )
            records.append(
                map(lambda x: x.encode(_UTF8), extract_data),
            )
        sorted_records = sorted(
            records,
            key=lambda x: datetime.strptime(x[-1], _ISO_FORMAT),
        )

        if not sorted_records:
            print("No Record.")
        else:
            for data, result, _ in sorted_records:
                line = "[{}][{}]".format(data, result)
                print(line)
