from __future__ import print_function
import os
import gzip
import inspect
from datetime import datetime
import xml.etree.ElementTree as ET
from functools import wraps
from pprint import pprint
from goslate import AdjustedGoslate

_UTF8 = 'UTF-8'
_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
_CACHE_FILE_NAME = 'cache.xml'
_RECORD_FILE_NAME = 'record.xml.gz'
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

def _debug_return_val(func):
    def _print_func(prefix, name):
        line = "{}: {}".format(prefix, name)
        print('*' * len(line))
        print(line)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._debug:
            _print_func('ENTER_FUNC', func.__name__)

        val = func(self, *args, **kwargs)

        if self._debug:
            _print_func('QUIT_FUNC', func.__name__)
            pprint(val)

        return val
    return wrapper


class Record:

    def __init__(self, debug=False):
        self._debug = debug
        # get path of search record
        self._dir_path = self._get_dir_path()

        self._cache_path = os.path.join(
            self._dir_path,
            _CACHE_FILE_NAME,
        )
        self._record_path = os.path.join(
            self._dir_path,
            _RECORD_FILE_NAME,
        )

    @_debug_return_val
    def _get_dir_path(self):
        dir = inspect.getmodule(self)
        path = dir.__file__
        dir_path, _ = os.path.split(path)
        return dir_path

    @_debug_return_val
    def _load_xml(self, file_path, gzip_enable=False):
        openfile = gzip.open if gzip_enable else open
        try:
            with openfile(file_path) as f:
                xml_content = f.read()
            xml = ET.fromstring(xml_content)
        except:
            # new one
            xml = ET.Element(_ROOT)
        return xml

    @_debug_return_val
    def _write_xml(self, xml, file_path,  gzip_enable=False):
        raw_xml = ET.tostring(xml, encoding=_UTF8)

        openfile = gzip.open if gzip_enable else open
        with openfile(file_path, 'wb') as f:
            f.write(raw_xml)

    @_debug_return_val
    def _judge_merge(self, file_path):
        # judge merge based on the file size(in bytes) pointed by file_path
        MAX_SIZE = 65535
        try:
            file_size = os.path.getsize(file_path)
        except:
            # file not exist, force to merge.
            file_size = MAX_SIZE + 1

        if file_size > MAX_SIZE:
            return True
        else:
            return False

    @_debug_return_val
    def _merge_records_from_cache(self, record_path, cache_path,
                                  force_merge=False):
        if not self._judge_merge(cache_path)\
                and not force_merge:
            return
        # merge file.
        record_xml = self._load_xml(self._record_path, gzip_enable=True)
        cache_xml = self._load_xml(self._cache_path)

        for node in cache_xml:
            record_xml.append(node)
        cache_xml.clear()

        self._write_xml(record_xml, self._record_path, gzip_enable=True)
        self._write_xml(cache_xml, self._cache_path)

    @_debug_return_val
    @_ensure_decode
    def add(self,
            from_lang,
            to_lang,
            data,
            result):

        # read xml record file
        cache_xml = self._load_xml(self._cache_path)

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
        sentence_node.text = result[AdjustedGoslate.SENTENCE]

        # multiple explanations
        if AdjustedGoslate.DICT in result:
            dict_node = ET.SubElement(result_node, _DICT)
            for pos, vals in result.get(AdjustedGoslate.DICT).items():
                pos_node = ET.SubElement(dict_node, _POS)
                # pos could be empty, I don't know why.
                pos_node.text = pos or 'error_pos'

                for val in vals:
                    meaning_node = ET.SubElement(pos_node, _MEANING)
                    meaning_node.text = val

        # save content to cache
        self._write_xml(cache_xml, self._cache_path)
        # judge merge
        self._merge_records_from_cache(self._record_path, self._cache_path)

    @_debug_return_val
    def display(self):
        # merge first
        self._merge_records_from_cache(
            self._record_path,
            self._cache_path,
            force_merge=True,
        )

        # targeting on record file
        record_xml = self._load_xml(self._record_path, gzip_enable=True)
        records = []
        for record in record_xml:
            extract_data = (
                record.find(_DATA).text,
                record.find(_RESULT).find(_SENTENCE).text,
                record.find(_TIME).text,
            )
            records.append(
                map(lambda x: x.encode(_UTF8), extract_data),
            )
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
