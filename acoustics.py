#!/usr/bin/env python
"""
	ACM Acoustics Media Player API Library
"""

import json, pycurl
import sys, urllib, time, os

reload(sys)
sys.setdefaultencoding("utf-8")

class AcousticsClient(object):
	def __init__(self, url):
		self.base_url    = url
		self.credentials = None
		self.client      = pycurl.Curl()
	def login(self, user, password):
		self.client.setopt(curl.USERPWD, "%s:%s" % (user, password))
		curl.setopt(curl.URL, "%s/www-data/auth" % (self.base_url))
		curl.perform()
		curl.close()


