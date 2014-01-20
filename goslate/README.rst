Goslate: Free Google Translate API
##################################################

.. contents:: :local:

``goslate`` provides you *free* python API to google translation service by querying google translation website.

It is:

- **Free**: you know it ;)
- **Fast**: batch, cache and concurrently fetch
- **Simple**: single file module, just ``Goslate().translate('Hi!', 'zh-CN')``


Usage
======

.. sourcecode:: python

 >>> import goslate
 >>> gs = goslate.Goslate()
 >>> print gs.translate('hello world', 'de')
 hallo welt

 
For batch translation, language detection, proxy support etc., please check `API reference <http://pythonhosted.org/goslate/#module-goslate>`_
 
 
Install
========

goslate support both Python2 and Python3. You could install it via:


.. sourcecode:: bash
  
  $ pip install goslate

 
or just download `latest goslate.py <https://bitbucket.org/zhuoqiang/goslate/raw/tip/goslate.py>`_ directly and use

`futures <https://pypi.python.org/pypi/futures>`_ is optional but recommended to install for best performance.


CLI
===========

``goslate.py`` is also a command line tool
    
- Translate ``stdin`` input into Chinese

  .. sourcecode:: bash
  
     $ echo "hello world" | goslate.py -t zh-CN

- Translate 2 text files into Chinese, output to UTF-8 file

  .. sourcecode:: bash
  
     $ goslate.py -t zh-CN -o utf-8 source/1.txt "source 2.txt" > output.txt

     
use ``--help`` for detail usage
     
.. sourcecode:: bash
  
   $ goslate.py -h
     
     
Contribute
===========     

- Report `issues & suggestions <https://bitbucket.org/zhuoqiang/goslate/issues>`_
- Fork `repository <https://bitbucket.org/zhuoqiang/goslate>`_
- `Donation <http://pythonhosted.org/goslate/#donate>`_
