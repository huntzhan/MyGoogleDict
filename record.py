from __future__ import print_function
import inspect
import os
from datetime import datetime
import xml.etree.ElementTree as ET


_UTF8 = 'UTF-8'


class Record:
    FILE_NAME = 'search_record'
    ROOT = 'root'
    RECORD = 'record'
    FROM_LANG = 'from_lang'
    TO_LANG = 'to_lang'
    DATA = 'data'
    RESULT = 'result'
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
            with open(xml_path) as f:
                xml_content = f.read()
            xml = ET.fromstring(xml_content)
        except:
            # new one
            xml = ET.Element(Record.ROOT)
        return xml

    def _write_xml(self, xml):
        raw_xml = ET.tostring(xml, encoding=_UTF8)
        with open(self._file_path, 'wb') as f:
            f.write(raw_xml)

    def add(self,
            from_lang,
            to_lang,
            data,
            result):

        # decodeing input source
        data = data.decode(_UTF8)
        # read xml record file
        record_xml = self._load_xml(self._file_path)

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
        result_node.text = result
        time_node.text = datetime.now().isoformat()

        # save content
        self._write_xml(record_xml)

    def display(self):
        record_xml = self._load_xml(self._file_path)
        records = []
        for record in record_xml:
            extract_data = (
                record.find(Record.DATA).text,
                record.find(Record.RESULT).text,
                record.find(Record.TIME).text,
            )
            records.append(
                map(lambda x: x.encode(_UTF8), extract_data),
            )
        sorted_records = sorted(
            records,
            key=lambda x: datetime.strptime(x[-1], "%Y-%m-%dT%H:%M:%S.%f"),
        )

        for data, result, _ in sorted_records:
            print(data, '\t', result)
