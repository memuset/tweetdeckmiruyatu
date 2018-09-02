# coding: utf-8

import console, json, os, pickle, ui, urllib.parse,webbrowser,time,threading
from objc_util import *
from threading import Timer

class BrowserView (ui.View):

	def eval_js(self, js):
		return self['webview'].evaluate_javascript(js)

	def get_url(self):
		return self.evaluate_javascript('window.location.href')

	def parse_url(self, url):
		return urllib.parse.urlparse(url).netloc
		
	def init_tweetbutton(self):
		button = self['tweet']
		button.image = ui.Image.named('./img1.png').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
		button.alpha = 0.0

	def init_webbrowser(self):
		web = self['webview']
		web.load_url('https://tweetdeck.twitter.com')
		web.delegate = self
		
	def init_size(self):
		# initialize with correct size when landscape
		orientation = ui.WebView(frame=(0,0,100,200)).eval_js('window.orientation')
		if orientation in (-90, 90):
			self.frame = (0, 0, self.height, self.width)

	def init_buttons(self):
			button = self['tweet']
			button.action = self.button_tapped
		
	#def init_refreshcontrol(self):
	#	UIRefreshControl = ObjCClass('UIRefreshControl')
	#	web = self['webview']
		#web.add_subview.UIRefreshControl

	def did_load(self):
		self.init_webbrowser()
		self.init_size()
	#	self.init_refreshcontrol()
		self.init_buttons()
		self.init_tweetbutton()
		self.flex = 'WH'
		self.webpage_has_loaded = False
		
	def touch_began(self, touch):
		print('began')
	def touch_moved(self, touch):
		print('moved')
	def touch_ended(self, touch):
		print('ended')
		
	def webview_should_start_load(self, webview, url, nav_type):	
		if 'twitter' not in url:
			UIApplication.sharedApplication()._openURL_(nsurl(url))
			return False
		else:
			return True
			
	def webview_did_finish_load(self, webview):
		timer = Timer(2.0, self.init_deck)
		thread_obj = threading.Thread(target=self.init_image)
		thread_obj.setDaemon(True)
		timer.start()
		thread_obj.start()
	
	def init_deck(self):
		self['tweet'].alpha = 1.0
		self.eval_js('document.getElementsByClassName("js-app-content app-content")[0].style.transitionDuration = 200+"ms";')
		self.eval_js('document.getElementsByClassName(\"application js-app is-condensed\")[0].classList.add(\'hide-detail-view-inline\');')
		self.eval_js('document.getElementsByClassName(\"js-app-header pin-all app-header is-condensed\")[0].style.display =\"none\";')
		self.eval_js('document.getElementsByClassName(\"js-app-content app-content\")[0].style.left = 0+\"px\";')
		
		column = self.eval_js('document.getElementsByClassName("js-column column").length;')
		
		for num in range(int(column)):			
			self.eval_js('document.getElementsByClassName("js-column column")[' + str(num) + '].style.width = 363+"px";')
		
	def init_image(self):
		while True:
			display = self.eval_js('document.getElementsByClassName("js-modal open-modal ovl scroll-v")[0].style.getPropertyValue("display");')
			
			if display == "block"	:
				self.eval_js('document.getElementsByClassName("js-med-tweet med-tweet")[0].style.right = 5+"%";')
				self.eval_js('document.getElementsByClassName("js-med-tweet med-tweet")[0].style.left = 5+"%";')
				self['tweet'].alpha = 0.0
				
			elif display == "none":
				self['tweet'].alpha = 1.0
			
			time.sleep(0.5)
	

	def button_tapped(self,sender):
		global now

		if now == 1 :
			self.open_tweet()
			now = 0				
			
		elif now == 0:
			self.close_tweet()
			now = 1
			
	def open_tweet(self):
		self.eval_js('document.getElementsByClassName(\"application js-app is-condensed\")[0].classList.remove(\'hide-detail-view-inline\');')
		self.eval_js('document.getElementsByClassName(\"js-app-content app-content\")[0].style.transform = \"translateX(0px)\";')
		self.eval_js('document.getElementsByClassName("js-app-content app-content")[0].style.marginRight = 0+"px";')
		
	def close_tweet(self):
		self.eval_js('document.getElementsByClassName(\"js-drawer drawer\")[1].classList.add(\'is-hidden\');')
		self.eval_js('document.getElementsByClassName("js-app-content app-content")[0].style.transform = "translateX(270px)";')
		

global now
now = 0
#UIRefreshControl = ObjCClass('UIRefreshControl')
view = 'iphone-full'
browser = ui.load_view(view)
browser.present(hide_title_bar=True,style='panel')
