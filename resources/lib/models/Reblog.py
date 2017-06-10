#!/usr/bin/python

class Reblog:
	def __init__(self, __type__, __name__, comment, __class__, tree_html):
		self.__type__ = __type__
		self.__name__ = __name__
		self.comment = comment
		self.__class__ = __class__
		self.tree_html = tree_html

