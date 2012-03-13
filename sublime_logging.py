import sublime
import sublime_plugin
import string, re, sys, os
import logging

class StatusBarLogHandler(logging.Handler):
	def __init__(self, key, view=None):
		logging.Handler.__init__(self)
		self.key = key
		self.view = view

	def emit(self, record):
		view = self.view
		if view is None:
			w = sublime.active_window()
			if w is not None:
				view = w.active_view()
			else:
				return
		display = self.format(record)
		view.set_status(self.key, str(display))
		# clear error after 5 seconds
		sublime.set_timeout(lambda: view.erase_status(self.key), 5000)
		return

class ViewLogHandler(logging.Handler):
	def __init__(self, name=None, view=None):
		logging.Handler.__init__(self)
		self.name = name
		self.view = None
		if type(view) == sublime.View:
			self.view = view
		return

	def find_view(self, name):
		for w in sublime.windows():
			for v in w.views():
				if v.name() == name:
					return v
		return None

	def emit(self, record):
		if self.view is None and self.name is not None:
			self.view = self.find_view(self.name)
		if self.view is None or self.view.window() is None:
			self.view = None
			w = sublime.active_window()
			if w is None:
				return
			self.view = w.new_file()
			self.view.set_scratch(True)
			if self.name is not None:
				self.view.set_name(self.name)
		display = self.format(record)
		self.view.set_read_only(False)
		edit = self.view.begin_edit()
		point = self.view.layout_to_text(self.view.layout_extent())
		self.view.insert(edit, point, str(display) + "\n")
		self.view.end_edit(edit)
		self.view.set_read_only(True)
		return

# do the heavy lifting
def getLogger(name, flush=False):
	log = logging.getLogger(name)
	if len(log.handlers) > 0:
		if not flush: return log
		for h in log.handlers:
			log.removeHandler(h)
	handler = ViewLogHandler(name='* ' + name + ' logs *')
	handler.setLevel(logging.DEBUG)
	handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s'))
	log.addHandler(handler)
	handler = StatusBarLogHandler(name)
	handler.setLevel(logging.ERROR)
	log.addHandler(handler)
	log.setLevel(logging.DEBUG)
	return log

class TestViewLogHandler(sublime_plugin.TextCommand):
	def run(self, edit):
		print 'testing status bar handler'
		self.test_viewlog()
	def test_viewlog(self):
		log = logging.getLogger('test_viewlog2')
		for h in log.handlers:
			log.removeHandler(h)
		handler = ViewLogHandler()
		handler.setLevel(logging.INFO)
		log.addHandler(handler)
		log.debug('Dont see this')
		log.error('This is an error and stuff')

class TestStatusBarLogHandler(sublime_plugin.TextCommand):
	def run(self, edit):
		print 'testing status bar handler'
		self.test_statusbar()
	
	def test_statusbar(self):
		log = logging.getLogger('test_statusbar')
		for h in log.handlers:
			log.removeHandler(h)
		handler = StatusBarLogHandler('test_statusbar')
		handler.setLevel(logging.ERROR)
		log.addHandler(handler)
		log.debug('Dont see this')
		log.error('This is an error and stuff')
