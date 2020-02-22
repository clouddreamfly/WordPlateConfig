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
		('images', ['images/wordplate.ico']), 
		('images/wp_bg', glob.glob('images/wp_bg/*.png')),
                ('images/heap_normal', glob.glob('images/heap_normal/*.png')),
                ('images/hand_small', glob.glob('images/hand_small/*.png')),
                ('images/hand_big', glob.glob('images/hand_big/*.png'))],
    zipfile = None,
) 


