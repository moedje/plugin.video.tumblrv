#!/usr/bin/python

class Photo(object):
	def __init__(self, caption, alt_sizes, original_size):
		self.caption = caption
		self.alt_sizes = alt_sizes
		self.original_size = original_size

