#!/usr/bin/python

class Blog:
	def __init__(self, __type__, __name__, share_likes, name, can_be_followed, active, theme, __class__, share_following):
		self.__type__ = __type__
		self.__name__ = __name__
		self.share_likes = share_likes
		self.name = name
		self.can_be_followed = can_be_followed
		self.active = active
		self.theme = theme
		self.__class__ = __class__
		self.share_following = share_following

