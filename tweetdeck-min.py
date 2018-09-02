# coding: utf-8

import console, json, os, pickle, ui, urllib.parse,webbrowser
from objc_util import *

class BrowserView (ui.View):

	def evaluate_javascript(self, js):
		return self['webview'].evaluate_javascript(js)
	
	def get_title(self):
		return self.evaluate_javascript('document.title')

	def get_url(self):
		return self.evaluate_javascript('window.location.href')

	def parse_url(self, url):
		return urllib.parse.urlparse(url).netloc

	def init_webbrowser(self):
		web = self['webview']
		web.load_url('https://tweetdeck.twitter.com')
		web.delegate = self
		
	def init_size(self):
		# initialize with correct size when landscape
		orientation = ui.WebView(frame=(0,0,100,200)).eval_js('window.orientation')
		if orientation in (-90, 90):
			self.frame = (0, 0, self.height, self.width)

	def did_load(self):
		self.init_webbrowser()
		self.init_size()
		self.flex = 'WH'
		self.webpage_has_loaded = False

		
	def webview_should_start_load(self, webview, url, nav_type):
		if 'twitter' not in url:
			UIApplication.sharedApplication()._openURL_(nsurl(url))
			return False
		else:
			return True

	def webview_did_start_load(self, webview):
		self.webpage_has_loaded = False
		

	def webview_did_finish_load(self, webview):
		self.webpage_has_loaded = True

view = 'iphone'
browser = ui.load_view(view)
browser.present(hide_title_bar=True,style='panel')

