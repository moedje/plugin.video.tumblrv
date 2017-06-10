#!/usr/bin/python

class User:
	def __init__(self, __type__, __name__, blogs, following, name, default_post_format, __class__, likes):
		self.__type__ = __type__
		self.__name__ = __name__
		self.blogs = blogs
		self.following = following
		self.name = name
		self.default_post_format = default_post_format
		self.__class__ = __class__
		self.likes = likes

