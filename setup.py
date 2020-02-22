#!/usr/bin/python
#-*-coding:utf-8-*-

from distutils.core import setup
import glob
import py2exe


options = {"py2exe":
	{"compressed": 1, #压缩  
		"optimize": 2, 
		"bundle_files": 1 #所有文件打包成一个exe文件
	}
}   

setup(
    windows = [{"script": "WordPlateConfig.py", "icon_resources": [(1, "images/wordplate.ico")]}],
	options = options,
	data_files = [
		('images',['images/wordplate.ico'])
		],
    zipfile = None,
) 


