#!/usr/bin/python

class Trail:
	def __init__(self, content_raw, is_root_item, post, is_current_item, blog, content):
		self.content_raw = content_raw
		self.is_root_item = is_root_item
		self.post = post
		self.is_current_item = is_current_item
		self.blog = blog
		self.content = content

