import logging
from subclim_logging import *
import sublime_plugin


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
