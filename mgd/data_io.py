from __future__ import print_function
import os
import gzip
import ConfigParser


_DEBUG = False


# _DATA_DIR hard coded the directory contains records and configuation file.
if _DEBUG:
    _DATA_DIR = '/Users/haoxun/Data/Project/MyGoogleDict/.mgd'
else:
    _DATA_DIR = os.path.expanduser('~/.mgd')

_CONFIG_FILENAME = 'config'
_CACHE_FILENAME = 'cache.xml'
_RECORD_FILENAME = 'record.xml.gz'


# fields in configuration file.
_SECTION_NAME = 'MyGoogleDict'
_FROM_LANG = 'default_from_lang'
_TO_LANG = 'default_to_lang'

# default content of configuration file.
_DEFAULT_CONFIG_CONTENT = """
[{section_name}]
{from_lang}: en
{to_lang}: zh-CN
""".format(
    section_name=_SECTION_NAME,
    from_lang=_FROM_LANG,
    to_lang=_TO_LANG,
)


class RecordIO(object):

    def __init__(self):
        self._cache_path = os.path.join(
            _DATA_DIR,
            _CACHE_FILENAME,
        )
        self._record_path = os.path.join(
            _DATA_DIR,
            _RECORD_FILENAME,
        )

    def _read_file(self, path, gzip_enable=False):
        openfile = gzip.open if gzip_enable else open
        with openfile(path) as f:
            content = f.read()
        return content

    def _write_file(self, content, path, gzip_enable=False):
        openfile = gzip.open if gzip_enable else open
        with openfile(path, 'wb') as f:
            f.write(content)

    ############
    # Cache IO #
    ############
    def _read_cache(self):
        return self._read_file(self._cache_path)

    def _write_cache(self, content):
        self._write_file(content, self._cache_path)

    cache = property(_read_cache, _write_cache)

    #############
    # Record IO #
    #############
    def _read_record(self):
        return self._read_file(self._record_path,
                               gzip_enable=True)

    def _write_record(self, content):
        self._write_file(content, self._record_path,
                         gzip_enable=True)

    record = property(_read_record, _write_record)

    ##############
    # Merge Flag #
    ##############
    def _judge_merge(self):
        # hardcode the threshold size of cache .
        MAX_SIZE = 65535
        try:
            file_size = os.path.getsize(self._cache_path)
        except:
            # file not exist, force to merge.
            file_size = MAX_SIZE + 1

        if file_size > MAX_SIZE:
            return True
        else:
            return False

    merge_flag = property(_judge_merge)


class ConfigIO:

    def __init__(self):
        self._config = ConfigParser.ConfigParser()
        self._config.readfp(self._open_config())

    def _init_config(self):
        # check existence of data dir.
        if not os.path.exists(_DATA_DIR):
            os.makedirs(_DATA_DIR)
        # check existence of configuration file
        path = os.path.join(_DATA_DIR, _CONFIG_FILENAME)
        if not os.path.exists(path):
            # generate default configuation file
            with open(path, 'w') as f:
                f.write(_DEFAULT_CONFIG_CONTENT)
        return path

    def _open_config(self):
        path = self._init_config()
        # return file
        return open(path)

    def set_up_doc(self, doc):
        return doc.format(
            default_from_lang=self._config.get(_SECTION_NAME, _FROM_LANG),
            default_to_lang=self._config.get(_SECTION_NAME, _TO_LANG),
        )


def set_up_doc(doc):
    config = ConfigIO()
    return config.set_up_doc(doc)
