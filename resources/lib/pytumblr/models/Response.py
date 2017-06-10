#!/usr/bin/python
class Response(object):
	def __init__(self, **kwargs):
		self.total_users = kwargs.get('total_users', None)
		self.users = kwargs.get('users', None)
		self.total_posts = kwargs.get('total_posts', 0)
		self.total_blogs = kwargs.get('total_blogs', 0)
		self.liked_count = kwargs.get('liked_count', 0)
		self.posts = kwargs.get('posts', [])
		self.blogs = kwargs.get('blogs', [])
		self.liked_posts = kwargs.get('liked_posts', [])

