import sublime
import sublime_plugin
import logging


def show_error_msg(msg):
    sublime.error_message(msg)


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

    def find_views(self, name):
        views = []
        for w in sublime.windows():
            for v in w.views():
                if v.name() == name:
                    views.append(v)
        return views

    # for some reason, if the tab isn't actually active, view.window() returns None
    # so we have to ask the windows if they have the view in them
    def view_active(self, view):
        for w in sublime.windows():
            g, idx = w.get_view_index(view)
            if g == -1 and idx == -1:
                continue
            return True
        # close the view, there's nothing to see here
        view.run_command('close')
        return False

    def create_view(self):
        w = sublime.active_window()
        if w is None:
            return
        v = w.new_file()
        v.set_scratch(True)
        if self.name is not None:
            v.set_name(self.name)
        return v

    def emit(self, record):
        # doing the write in an EventHandler makes ST2 crash
        # so we queue the write out to the main thread
        sublime.set_timeout(lambda: self.write(self.view, record), 50)
        return

    # is there a way to make the edit without forcing the view to activate?
    def write(self, view, record):
        # if we don't yet have an active window, then we really can't log the message
        if sublime.active_window() is None:
            return

        # if we don't know where we're writing to, find it
        if self.view is None and self.name is not None:
            candidates = self.find_views(self.name)
            # print(candidates)
            if len(candidates) > 0:
                self.view = candidates[0]

        # if we still don't know where we're writing to, make it
        # or if the window was previously closed, create a new one
        if self.view is None or not self.view_active(self.view):
            self.view = self.create_view()

        # insert text
        display = self.format(record)
        self.view.run_command('write_log_to_new_file', {'output': display})
        return


def getLogger(name, flush=False):
    '''do the heavy lifting'''
    log = logging.getLogger(name)

    # if we have already set up logging
    if len(log.handlers) > 0:
        if not flush:
            return log
        for h in log.handlers:
            log.removeHandler(h)
    fmt = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')

    # add in a ViewLogHandlder
    handler = ViewLogHandler(name='* ' + name + ' logs *')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(fmt)
    log.addHandler(handler)

    # add in a status bar handler for errors
    handler = StatusBarLogHandler(name)
    handler.setLevel(logging.ERROR)
    log.addHandler(handler)

    # add in a file handler
    # handler = logging.FileHandler(os.environ['HOME'] + '/' + name + '.log','a')
    # handler.setLevel(logging.DEBUG)
    # handler.setFormatter(fmt)
    # log.addHandler(handler)

    # log.setLevel(logging.DEBUG)
    log.setLevel(logging.ERROR)
    return log


class WriteLogToNewFile(sublime_plugin.TextCommand):
    '''write log output to a new file'''

    def run(self, edit, output):
        self.view.set_read_only(False)
        point = self.view.layout_to_text(self.view.layout_extent())
        self.view.insert(edit, point, str(output) + "\n")
        self.view.set_read_only(True)
        point = self.view.layout_to_text(self.view.layout_extent())
        self.view.show(point)
