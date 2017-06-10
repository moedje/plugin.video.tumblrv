#!/usr/bin/python

class Note(object):
	def __init__(self, blog_uuid, avatar_shape, blog_url, type, followed, blog_name, timestamp):
		self.blog_uuid = blog_uuid
		self.avatar_shape = avatar_shape
		self.blog_url = blog_url
		self.type = type
		self.followed = followed
		self.blog_name = blog_name
		self.timestamp = timestamp

