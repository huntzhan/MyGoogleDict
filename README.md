#Requirement

MyGoogleDict is a command line tool which communicates with google translation server. With the consideration of my personal needs, MyGoogleDict should fulfill the requirements as follow:

1. Communicate with [translate.google.com](translate.google.com) for translation bussiness.
1. Support various languages.
1. Support translation of both a single word and multi-words sentences.
1. Record and display the search history of user.
1. Human readable manual in command line interface.

#Design

##Depandancy and Resoureces

###docopt
[docopt](https://github.com/docopt/docopt) is adopt for parsing the command arguments.

###goslate
[goslate](http://pythonhosted.org/goslate/) handles the communication with google translation server.


##Bussiness
The bussiness logic is quite simple. As MyGoogleDict is a command line program, the bussiness logic is roughly determined by the arguments and options entered by user.

Here is the avaliable inputs:

	Usage: mgd [-f <from_lang>] [-t <to_lang>] [-v|--reverse] <data>
       	   mgd -r|--record
       	   mgd -h|--help

	Options:
    	-f <from_lang>  input language [default: en]
    	-t <to_lang>    ouput language [default: zh-CN]
    	-v --reverse    reverse -f and -t
    	-r --record     display search record
    	
where <from_lang> and <to_lang> should be the language arguments, should be found in a list of [avaliable languages](https://developers.google.com/translate/v2/using_rest#language-params) of google translation serve.

##Implementation
Directory MyGoogleDict contains following files:

* **interface.py** for the job of argument parsing.
* **translate.py** for the translation logic.
* **record.py** for reading and writing search records.


##Deployment
First, make sure that you can execute **interfact.py**:

	$ chmod +x interface.py

Then, make a symbolic link in your PATH(/usr/local/bin is recommended) which points to **interface.py**, for example:
	
	$ ln -s interface.py /usr/local/bin/mgd

where mgd is the abbreviation of MyGoogleDict.

##Usage
Example of usage:

	$ mgd -r
	No Record.
	$ mgd test
	[verb] 检验, 试, 考, 测验, 验, 考查, 尝
	[noun] 测试, 试验, 试, 实验, 考试, 考验, 测验
	$ mgd -t ja test
	[verb] 試す, 試みる
	[noun] テスト, 試験, 試し, 試練, 考査
	$ mgd -f zh-CN -t en 测试
	[noun] test, examination
	$ mgd -r
	[test][测试]
	[test][テスト]
	[测试][Test]

