from __future__ import unicode_literals
from __future__ import print_function

import os
import gzip

try:
    import ConfigParser as configparser
except:
    import configparser

# __DATA_DIR hard coded the directory contains records and configuation
# file.
_DATA_DIR = os.path.expanduser('~/.mgd')

_CONFIG_FILENAME = 'config'
_CACHE_FILENAME = 'cache.xml'
_RECORD_FILENAME = 'record.xml.gz'

# fields in configuration file.
_SECTION_NAME = 'MyGoogleDict'
_FROM_LANG = 'default_from_lang'
_TO_LANG = 'default_to_lang'
_AUDIO_PLAYBACK_COMMAND = 'audio_playback_command'

_RAW_CONTENT = """
[{}]
{}: en
{}: zh-CN
{}: {}
"""


def _generate_default_config_content():
    import platform
    audio_player = 'afplay' if platform.system() == 'Darwin' else 'mpg123'

    content = _RAW_CONTENT.format(
        _SECTION_NAME,
        _FROM_LANG,
        _TO_LANG,
        _AUDIO_PLAYBACK_COMMAND, audio_player,
    )
    return content

_DEFAULT_CONFIG_CONTENT = _generate_default_config_content()


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
        """
        Parameters:
            path: points to file to be read.
            gzip_enable: Ture for using gzip.open(), False for using built-in
                         open().
        Return:
            Content of file represented in bytes.
        """

        openfile = gzip.open if gzip_enable else open
        with openfile(path, 'rb') as f:
            content = f.read()
        return content

    def _write_file(self, content, path, gzip_enable=False):
        """
        Parameters:
            content: bytes of content to be written to file.
            others: equivalent to _read_file.
        Return:
            None.
        """

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
        """
        Return:
            True for merging file.
        """

        # hardcode the threshold size of cache .
        MAX_SIZE = 65535
        try:
            file_size = os.path.getsize(self._cache_path)
        except:
            # file not exist, force to merge.
            return True

        if file_size > MAX_SIZE:
            return True
        else:
            return False

    merge_flag = property(_judge_merge)


class ConfigIO(object):

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.readfp(self._open_config())

    def _init_config(self):
        # check existence of data dir.
        if not os.path.exists(_DATA_DIR):
            os.makedirs(_DATA_DIR)

        path = os.path.join(
            _DATA_DIR,
            _CONFIG_FILENAME,
        )
        # assure existence of configuration file
        if not os.path.exists(path):
            # generate default configuation file.
            # text mode is required, for writing unicode literals.
            with open(path, 'w') as f:
                f.write(_DEFAULT_CONFIG_CONTENT)
        # finally, return that path.
        return path

    def _open_config(self):
        path = self._init_config()
        # return file object, with default mode wt.
        return open(path)

    def set_up_doc(self, doc):
        return doc.format(
            default_from_lang=self._config.get(_SECTION_NAME,
                                               _FROM_LANG),
            default_to_lang=self._config.get(_SECTION_NAME,
                                             _TO_LANG),
        )

    def get_playback_command(self):
        return self._config.get(_SECTION_NAME,
                                _AUDIO_PLAYBACK_COMMAND)


def set_up_doc(doc):
    config_io = ConfigIO()
    return config_io.set_up_doc(doc)


def get_playback_command():
    config_io = ConfigIO()
    raw_command = config_io.get_playback_command()
    return raw_command.split(' ')
