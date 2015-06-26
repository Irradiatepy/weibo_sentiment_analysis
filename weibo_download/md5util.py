# -*- coding:utf-8 -*-
import sys
import hashlib
import types
reload(sys)
sys.setdefaultencoding('utf-8')

def md5(str):
	if type(str) is types.StringType:
		m = hashlib.md5()
		m.update(str)
		return m.hexdigest()
	else:
		return ''

def main():
	print md5('jing***')

if __name__ == '__main__':
	main()