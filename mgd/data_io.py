import os
import ConfigParser

_DEBUG = True

# _DATA_DIR hard coded the directory contains records and configuation file.
if _DEBUG:
    _DATA_DIR = '/Users/haoxun/Data/Project/MyGoogleDict/.mgd'
else:
    _DATA_DIR = '~/.mgd'
_CONFIG_FILENAME = 'config'
_CACHE_FILENAME = 'cache.xml'
_RECORD_FILENAME = 'record.xml.gz'

# fields in configuration file.
_SECTION_NAME = 'MyGoogleDict'
_FROM_LANG = 'default_from_lang'
_TO_LANG = 'default_to_lang'
# default content of configuration file.
_DEFAULT_CONFIG_CONTENT =\
"""
[{section_name}]
{from_lang}: en
{to_lang}: zh-CN
""".format(
    section_name=_SECTION_NAME,
    from_lang=_FROM_LANG,
    to_lang=_TO_LANG,
)


class RecordIO:
    pass


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
