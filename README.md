#Requirement

MyGoogleDict is a command-line program which communicates with google translation server. With the consideration of my personal needs, MyGoogleDict should fulfill the requirements as follow:

1. Communicate with [translate.google.com](http://translate.google.cn/) for translation bussiness.
1. Support translation of various languages.
1. Support translation of both a single word and multi-words sentences. Moreover, the program should classify results of translation with respect to their part of speech.
1. Record and display the search history of user.
1. Human readable manual in command line interface.

#Design

##Depandancy and Resoureces

Depandancies of the program are as follows:

* [docopt](https://github.com/docopt/docopt) v0.6.1 is adopt for parsing arguments.
* [google_translate_api](https://github.com/haoxun/GoogleTranslateAPI) v0.2 handles the communication with google translation server.


##Bussiness
The bussiness logic is quite simple. As MyGoogleDict is a command line program, the bussiness logic is roughly determined by the arguments and options entered by user.

Here is the avaliable inputs:

	Usage: mgd [-f <from_lang>] [-t <to_lang>]
	           [-v|--reverse] [-s|--speak] <data>...
	       mgd -r|--record
	
	Options:
	    -f <from_lang>  input language [default: en]
	    -t <to_lang>    ouput language [default: zh-CN]
	    -v --reverse    reverse -f and -t
	    -r --record     display search record
	    -s --speak      speak out the result



    	
where the value of language arguments <from_lang> and <to_lang> could be found in a list of [avaliable languages variable](https://developers.google.com/translate/v2/using_rest#language-params).

#Implementation
## Code Files
Directory MyGoogleDict contains following files:

* **interface.py** for the job of argument parsing.
* **translate.py** for the translation logic.
* **record.py** for reading and writing search records.
* **share.py** for shared code.
* **data_io.py** for read/write records and configurations.

## Release and To-Do List
### To-Do List
#### 0.3
* Introduce more error dectection strategy, such as dectecting misspelling input.
* Design record management strategy.
* Design a well-formatted user report which displays user's searching history in a period(maybe a month).
* Implement unit tests.
* *nix standard IO support.
* Detect the input language automatically.

### Release List
#### 0.2
* Change dependency from goslate to google_translate_api.
* Enable TTS service.

#### 0.1 

* Implement basic functionality, such as display the result of translation, read and write records.
* Packaged and uploaded the project, enable user to download it through 'pip install' command.



#Installation

	pip install mgd


##Data Storage and Configuration

Records and configuration file would be stored in **~/.mgd/**:

* **~/.mgd/config** stroes the configuration of mgd. Currently, you can configure the default languages of the program.
* **~/.mgd/cache.xml** serves as a cache to record.xml.gz.
* **~/.mgd/record.xml.gz** stores records in xml.gz format.


#Usage
Example of usage:

	$ mgd -r
	No Record.
	$ mgd test
	[verb] 检验, 试, 考, 测验, 验, 考查, 尝
	[noun] 测试, 试验, 试, 实验, 考试, 考验, 测验
	$ mgd -s test
	[verb] 检验, 试, 考, 测验, 验, 考查, 尝
	[noun] 测试, 试验, 试, 实验, 考试, 考验, 测验
	$ mgd -t ja test
	[verb] 試す, 試みる
	[noun] テスト, 試験, 試し, 試練, 考査
	$ mgd -f zh-CN -t en 测试
	[noun] test, examination
	$ mgd -v 测试
	[noun] test, examination
	$ mgd this is a sentence.
	[sentence] 这是一个句子。
	$ mgd -r
	[test][测试]
	[test][测试]
	[test][テスト]
	[测试][Test]
	[测试][Test]
	[this is a sentence.][这是一个句子。]

