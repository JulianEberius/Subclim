'''Integrates ST2 with Eclim running in an Eclipse instance.
Enables Java completions / go to definition etc'''
import sublime_plugin
import sublime
import re
import os
import json
import threading

try:
    # Python 3
    from . import eclim
    from . import subclim_logging
    import queue
except (ValueError):
    # Python 2
    import eclim
    import subclim_logging
    import Queue as queue

log = subclim_logging.getLogger('subclim')
settings = sublime.load_settings("Subclim.sublime-settings")
auto_complete = settings.get("subclim_auto_complete", True)


def auto_complete_changed():
    global auto_complete
    auto_complete = settings.get("subclim_auto_complete", True)
settings.add_on_change("subclim_auto_complete", auto_complete_changed)


def offset_of_location(view, location):
    '''we should get utf-8 size in bytes for eclim offset'''
    text = view.substr(sublime.Region(0, location))
    cr_size = 0
    if view.line_endings() == 'Windows':
        cr_size = text.count('\n')
    return len(text.encode('utf-8')) + cr_size


# worker thread for async tasks
def worker():
    while True:
        task = tasks.get()
        try:
            task()
        except:
            import traceback
            traceback.print_exc()
        finally:
            tasks.task_done()
tasks = queue.Queue()
t = threading.Thread(target=worker)
t.daemon = True
t.start()


def flatten_command_line(lst):
    '''shallow flatten for sequences of strings'''
    return [i for sub in lst for i in ([sub] if isinstance(sub, basestring) else sub)]


class UnknownSubclimTemplateHandlerException(Exception):
    pass


class SubclimBase(object):
    def __init__(self, *args, **kwargs):
        self.template_handler = SubclimBase.DEFAULT_HANDLER.copy()

    def is_configured(self):
        return check_eclim()

    def find_view(self, view):
        if type(view) == sublime.View:
            return view
        view = getattr(self, 'view', None)
        if type(view) == sublime.View:
            return view
        window = getattr(self, 'window', None)
        if type(window) == sublime.Window:
            return window.active_view()
        return sublime.active_window().active_view()

    def get_relative_path(self, flag, view):
        return (flag, get_context(view)[1])

    def get_project(self, flag, view):
        return (flag, get_context(view)[0])

    def get_cursor(self, flag, view):
        return (flag, str(view.sel()[0].a))

    def get_selection_start(self, flag, view):
        s = view.sel()
        if len(s) == 1 and s[0].a == s[0].b:
            return (flag, '0')
        e = min([min(i.a, i.b) for i in s])
        return (flag, str(e))

    def get_selection_end(self, flag, view):
        s = view.sel()
        if len(s) == 1 and s[0].a == s[0].b:
            return (flag, str(view.layout_to_text(view.layout_extent())))
        e = max([max(i.a, i.b) for i in s])
        return (flag, str(e))

    def get_encoding(self, flag, view):
        enc = view.encoding()
        if enc == "Undefined":
            enc = "utf-8"
        return (flag, enc)

    def get_classname(self, flag, view):
        return (flag, os.path.splitext(view.file_name())[0])

    def build_template(self, template, view=None, **kwargs):
        view = self.find_view(view)
        k = template.keys()[0]
        handler = getattr(self, 'template_handler', SubclimBase.DEFAULT_HANDLER)
        cmdline = ['-command', k]
        for param in template[k]:
            scrub = param.replace('[', '').replace(']', '')
            if ' ' in scrub:
                flag, _ = scrub.split(' ', 1)
            else:
                flag = scrub
            # ignore optional parameters
            if param not in handler:
                if param.startswith('['):
                    log.warn('ignoring missing optional parameter: %s', param)
                    continue
                if flag in kwargs:
                    continue
                log.error('error finding paramter: %s', param)
                raise UnknownSubclimTemplateHandlerException(param)
            cmdline.append(handler[param](self, flag, view))
        return cmdline

    def get_additional_args(self, d):
        '''if we've been passed command line options, add them in'''
        return [((k, v) if v is not None else k) for k, v in d.items() if k.startswith('-')]

    def run_template(self, template, view=None, **kwargs):
        cmdline = self.build_template(template, view, **kwargs)
        cmdline.extend(self.get_additional_args(kwargs))
        return self.run_eclim(cmdline)

    def run_eclim(self, cmdline):
        log.info(cmdline)
        flat = flatten_command_line(cmdline)
        return eclim.call_eclim(flat)

    # each handler called with self, flag, view
    DEFAULT_HANDLER = {
        '-f file': get_relative_path,
        '-p project': get_project,
        '-o offset': get_cursor,
        '-b boffset': get_selection_start,
        '-e eoffset': get_selection_end,
        '-e encoding': get_encoding
        # '-c class' : get_classname
    }


class EclimCommand(sublime_plugin.TextCommand, SubclimBase):
    '''To be run from the python console or other nefariousness'''
    def run(self, edit, **kwargs):
        cmdline = self.get_additional_args(kwargs)
        self.run_eclim(cmdline)


def check_eclim_version():
    out = SubclimBase.run_template({"ping": []}, {})
    m = re.search(r'^eclim\s+(.*)$', out, re.MULTILINE)
    version = int("".join(m.group(1).split(".")))
    if version < 173:
        sublime.error_message("Subclim depends on Eclim 1.7.3 or higher. Please update your Eclim installation.")


def initialize_eclim_module():
    '''Loads the eclim executable path from ST2's settings and sets it
    in the eclim module'''
    s = sublime.load_settings("Subclim.sublime-settings")
    eclim_executable = s.get("eclim_executable_location", None)
    # log.debug('eclim_executable = ' + eclim_executable)
    eclim.eclim_executable = eclim_executable

# when this module is loaded (by ST2), initialize the eclim module
initialize_eclim_module()


def check_eclim(view=None):
    if not eclim.eclim_executable:
        initialize_eclim_module()
    if not eclim.eclim_executable:
        log.error("Eclim executable path not set, call the set_eclim_path command!")
        return False
    return True


def get_context(view):
    s = view.settings()
    project = s.get('subclim.project', None)
    relative_path = s.get('subclim.project_relative_path', None)
    if project is None:
        project, relative_path = eclim.get_context(view.file_name())
        if project is not None:
            s.set('subclim.project', project)
        if relative_path is not None:
            s.set('subclim.project_relative_path', relative_path)
    return project, relative_path


def get_classname(view):
    s = view.settings()
    klass = s.get('subclim.classname', None)
    if klass is None:
        # todo
        return None
    return klass


class SetEclimPath(sublime_plugin.WindowCommand):
    '''Asks the user for the path to the Eclim executable and saves it in
    ST2's prefernces'''
    def run(self):
        default_path = "/path/to/your/eclipse/eclim"
        initialize_eclim_module()
        if eclim.eclim_executable is not None:
            default_path = eclim.eclim_executable

        self.window.show_input_panel(
            "Input path to eclim executable (in your eclipse directory)",
            default_path, self.path_entered, None, None)

    def path_entered(self, path):
        path = os.path.abspath(os.path.expanduser(path))
        s = sublime.load_settings("Subclim.sublime-settings")
        s.set("eclim_executable_location", path)
        sublime.save_settings("Subclim.sublime-settings")
        # re-initialize the eclim module with the new path
        initialize_eclim_module()


class SubclimGoBack(sublime_plugin.TextCommand):

    navigation_stack = []

    def run(self, edit, block=False):
        if len(SubclimGoBack.navigation_stack) > 0:
            self.view.window().open_file(
                SubclimGoBack.navigation_stack.pop(),
                sublime.ENCODED_POSITION)


class JavaGotoDefinition(sublime_plugin.TextCommand):
    '''Asks Eclipse for the definition location and moves ST2 there if found'''

    def run(self, edit, block=False):
        if not check_eclim(self.view):
            return
        project, file = get_context(self.view)
        pos = self.view.sel()[0]
        word = self.view.word(pos)
        offset = offset_of_location(self.view, word.a)
        locations = self.call_eclim(project, file, offset, word.size())
        locations = self.to_list(locations)

        #  one definition was found and it is in a java file -> go there
        if len(locations) == 1:
            if locations[0]['filename'].endswith("java"):
                self.go_to_location(locations[0])
                return

        # we didnt return correctly, display error in statusbar
        error_msg = "Could not find definition of %s" % self.view.substr(word)
        log.error(error_msg)

    def call_eclim(self, project, filename, offset, ident_len, shell=True):
        eclim.update_java_src(project, filename)

        go_to_cmd = ['-command', 'java_search',
                     '-n', project,
                     '-f', filename,
                     '-o', str(offset),
                     '-e', 'utf-8',
                     '-l', str(ident_len)]
        out = eclim.call_eclim(go_to_cmd)
        return out

    def to_list(self, locations):
        return json.loads(locations)

    def go_to_location(self, loc):
        # save current position
        row, col = self.view.rowcol(self.view.sel()[0].a)
        SubclimGoBack.navigation_stack.append("%s:%d:%d" % (
            self.view.file_name(), row + 1, col + 1))

        # go to new position
        f, l, c = loc['filename'], loc['line'], loc['column']
        path = "%s:%s:%s" % (f, l, c)
        sublime.active_window().open_file(path, sublime.ENCODED_POSITION)


class JavaGotoUsages(JavaGotoDefinition):
    '''Asks Eclipse for the usage locations and moves ST2 there if found'''
    def run(self, edit, block=False):
        if not check_eclim(self.view):
            return
        project, file = get_context(self.view)
        pos = self.view.sel()[0]
        word = self.view.word(pos)
        offset = offset_of_location(self.view, word.a)
        locations = self.call_eclim(project, file, offset, word.size())
        locations = self.to_list(locations)

        if len(locations) == 1:
            #  one definition was found and it is in a java file -> go there
            if locations[0]['filename'].endswith("java"):
                self.go_to_location(locations[0])
                return
        else:
            #  multiple usages -> show menu
            self.locations = locations
            self.view.window().show_quick_panel(
                [l['message'] for l in self.locations],
                self.location_selected, sublime.MONOSPACE_FONT)

    def location_selected(self, selected_idx):
        self.go_to_location(self.locations[selected_idx])

    def call_eclim(self, project, filename, offset, ident_len, shell=True):
        eclim.update_java_src(project, filename)

        go_to_cmd = ['-command', 'java_search',
                     '-n', project,
                     '-f', filename,
                     '-o', str(offset),
                     '-e', 'utf-8',
                     '-l', str(ident_len),
                     '-x', 'references']
        out = eclim.call_eclim(go_to_cmd)
        return out


class RunClass(object):
    def get_arguments(self, callback):
        s = self.view.settings()
        last_args = s.get('subclim.last_arguments', "")

        def save_and_callback(response):
            s.set('subclim.last_arguments', response)
            callback(response)

        self.view.window().show_input_panel(
            "Arguments",
            last_args, save_and_callback, None, None)

    def display_in_view(self, doc):
        window = self.view.window()
        create_view_in_same_group = False

        v = self.find_runclass_view()
        if not v:
            active_group = window.active_group()
            if not create_view_in_same_group:
                if window.num_groups() == 1:
                    window.run_command('new_pane', {'move': False})
                if active_group == 0:
                    window.focus_group(1)
                else:
                    window.focus_group(active_group-1)

            window.new_file(sublime.TRANSIENT)
            v = window.active_view()
            v.set_name("*run_output*")
            v.set_scratch(True)

        v.set_read_only(False)
        v.run_command("simple_clear_and_insert", {"insert_string": doc})
        v.set_read_only(True)
        window.focus_view(v)

    def find_runclass_view(self):
        '''
        Return view named *run_output* if exists, None otherwise.
        '''
        for w in self.view.window().views():
            if w.name() == "*run_output*":
                return w
        return None

    def call_eclim(self, project, file_name, class_name, args=""):
        eclim.update_java_src(project, file_name)
        go_to_cmd = ['-command', 'java', '-p', project, '-c', class_name, '-a'] + args.split(" ")
        out = eclim.call_eclim(go_to_cmd)
        return out


class JavaRunClass(sublime_plugin.TextCommand, RunClass):
    '''Runs the current class as Java program, good for testing
    small Java-"Scripts"'''

    def run(self, edit, block=False):
        if not check_eclim(self.view):
            return
        project, file_name = get_context(self.view)
        class_name, _ = os.path.splitext(os.path.basename(file_name))
        package_name = self.find_package_name()
        if package_name:
            class_name = package_name + "." + class_name

        def callback(args):
            self.display_in_view("Running %s with %s" % (class_name, " ".join(args)))

            def run_task():
                result = self.call_eclim(project, file_name, class_name, args)
                self.display_in_view(result)
            tasks.put(run_task)

        self.get_arguments(callback)

    def find_package_name(self):
        '''Searches the current file line by line for the
        package definition.'''
        line_regions = self.view.split_by_newlines(
            sublime.Region(0, self.view.size()))
        for line_region in line_regions:
            line = self.view.substr(line_region)
            m = re.search(r'package ([^;]*);', line)
            if m:
                return m.group(1)
        return None


class ScalaRunClass(sublime_plugin.TextCommand, RunClass):
    '''Runs the current class as Scala program, good for testing
    small Scala-"Scripts"'''

    def run(self, edit, block=False):
        if not check_eclim(self.view):
            return

        project, file_name = get_context(self.view)
        class_name = self.find_qualified_scala_name()

        def callback(args):
            self.display_in_view("Running %s with %s" % (class_name, args))

            def run_task():
                result = self.call_eclim(project, file_name, class_name, args)
                self.display_in_view(result)
            tasks.put(run_task)

        self.get_arguments(callback)

    def find_qualified_scala_name(self):
        line_regions = self.view.split_by_newlines(
            sublime.Region(0, self.view.sel()[0].a))

        for line_region in reversed(line_regions):
            line = self.view.substr(line_region)
            m = re.search(r'object ([^\s]*)', line)
            if not m:
                continue
            class_name = m.group(1)
            for line_region in line_regions:
                line = self.view.substr(line_region)
                m = re.search(r'package (.*)$', line)
                if not m:
                    return
                package_name = m.group(1)
                return package_name + "." + class_name


class CompletionProposal(object):
    def __init__(self, name, insert=None, type="None"):
        split = name.split(" ")
        self.name = "%s\t%s" % (split[0], " ".join(split[1:]))
        self.display = self.name
        if insert:
            self.insert = insert
        else:
            self.insert = name
        self.type = "None"

    def __repr__(self):
        return "CompletionProposal: %s %s" % (self.name, self.insert)


class ManualCompletionRequest(sublime_plugin.TextCommand):
    '''Used to request a full Eclim autocompletion when
    auto_complete is turned off'''
    def run(self, edit, block=False):
        JavaCompletions.user_requested = True
        self.view.run_command("save")
        self.view.run_command('auto_complete', {
                              'disable_auto_insert': True,
                              'api_completions_only': True,
                              'next_completion_if_showing': False,
                              })


class JavaCompletions(sublime_plugin.EventListener):
    '''Java/Scala completion provider'''
    # set when the just requested a manual completion, else False
    user_requested = False

    def on_query_completions(self, view, prefix, locations):
        if not (auto_complete or JavaCompletions.user_requested):
            return []
        JavaCompletions.user_requested = False

        c_func = self.complete_func(view)
        if not c_func:
            return []
        if not check_eclim(view):
            return []
        # if we haven't saved yet, push the auto complete to the main thread
        if view.is_dirty():
            sublime.set_timeout(lambda: self.queue_completions(view), 0)
            return []
        project, fn = get_context(view)
        pos = offset_of_location(view, locations[0])

        proposals = self.to_proposals(c_func(project, fn, pos))
        return [(p.display, p.insert) for p in proposals]

    def queue_completions(self, view):
        view.run_command("save")
        view.run_command('auto_complete', {
                         'disable_auto_insert': True,
                         'api_completions_only': True,
                         'next_completion_if_showing': False,
                         })

    def complete_func(self, view):
        syntax = view.settings().get("syntax")
        if "Java.tmLanguage" in syntax:
            return self.call_eclim_java
        elif "Scala.tmLanguage" in syntax:
            return self.call_eclim_scala
        else:
            return None

    def call_eclim_java(self, project, file, offset, shell=True):
        eclim.update_java_src(project, file)
        complete_cmd = "-command java_complete \
                                -p %s \
                                -f %s \
                                -o %i \
                                -e utf-8 \
                                -l compact" % (project, file, offset)
        out = eclim.call_eclim(complete_cmd)
        return out

    def call_eclim_scala(self, project, file, offset, shell=True):
        eclim.update_scala_src(project, file)
        complete_cmd = "-command scala_complete \
                                -p %s \
                                -f %s \
                                -o %i \
                                -e utf-8 \
                                -l compact" % (project, file, offset)
        out = eclim.call_eclim(complete_cmd)
        return out

    def to_proposals(self, eclim_output):
        proposals = []

        completions = json.loads(eclim_output)
        # newer versions of Eclim package the list of completions in a dict
        if isinstance(completions, dict):
            completions = completions['completions']
        for c in completions:
            if not "<br/>" in c['info']:  # no overloads
                proposals.append(CompletionProposal(c['info'], c['completion']))
            else:
                variants = c['info'].split("<br/>")
                param_lists = [re.search(r'\((.*)\)', v) for v in variants]
                param_lists = [x.group(1) for x in param_lists if x]
                props = []
                for idx, pl in enumerate(param_lists):
                    if pl:
                        params = [par.split(" ")[-1] for par in pl.split(", ")]
                        insert = ", ".join(["${%i:%s}" % (i, s)
                                            for i, s in
                                            zip(range(1, len(params) + 1), params)
                                            ])
                        insert = c['completion'] + insert + ")"
                        props.append(CompletionProposal(variants[idx], insert))
                    else:
                        props.append(CompletionProposal(variants[idx], c['completion']))
                proposals.extend(props)
        return proposals


class JavaValidation(sublime_plugin.EventListener):
    '''Show Java errors as found by Eclipse on save and load.
    Will trigger Eclipse compiles.'''

    drawType = 4 | 32
    line_messages = {}

    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)
        self.lastCount = {}

    def validation_func(self, view):
        syntax = view.settings().get("syntax")
        if "Java.tmLanguage" in syntax:
            return eclim.update_java_src
        elif "Scala.tmLanguage" in syntax:
            return eclim.update_scala_src
        else:
            return None

    def on_load(self, view):
        validation_func = self.validation_func(view)
        if validation_func:
            buf_id = view.buffer_id()

            def validation_closure():
                try:
                    v = sublime.active_window().active_view()
                except AttributeError:
                    pass
                if v.buffer_id() == buf_id:
                    self.validate(view, validation_func)

            sublime.set_timeout(validation_closure, 1500)

    def on_post_save(self, view):
        validation_func = self.validation_func(view)
        if validation_func:
            self.validate(view, validation_func)

            # sometimes, Eclipse will not report errors instantly
            # check again a bit later
            def validation_closure():
                self.validate(view, validation_func)
            sublime.set_timeout(validation_closure, 1500)

    def validate(self, view, validation_func):
        if not check_eclim(view):
            return
        project, file = get_context(view)
        problems = {}

        def async_validate_task():
            out = validation_func(project, file)
            problems.update(eclim.parse_problems(out))
            sublime.set_timeout(on_validation_finished, 0)

        def on_validation_finished():
            line_messages = JavaValidation.line_messages
            vid = view.id()
            line_messages[vid] = {}
            for e in problems['errors']:
                l_no = int(e['line'])
                if not line_messages[vid].get(l_no, None):
                    line_messages[vid][l_no] = []
                line_messages[vid][l_no].append(e)
            self.visualize(view)
            self.on_selection_modified(view)

        tasks.put(async_validate_task)

    def visualize(self, view):
        view.erase_regions('subclim-errors')
        view.erase_regions('subclim-warnings')
        lines = JavaValidation.line_messages[view.id()]

        outlines = [view.line(view.text_point(lineno - 1, 0))
                    for lineno in lines.keys()
                    if len(list(filter(lambda x: x['error'], lines[lineno]))) > 0]
        view.add_regions(
            'subclim-errors', outlines, 'keyword', 'dot', JavaValidation.drawType)

        outlines = [view.line(view.text_point(lineno - 1, 0))
                    for lineno in lines.keys()
                    if len(list(filter(lambda x: x['error'], lines[lineno]))) <= 0]
        view.add_regions(
            'subclim-warnings', outlines, 'comment', 'dot', JavaValidation.drawType)

    def on_selection_modified(self, view):
        validation_func = self.validation_func(view)
        if validation_func:
            line_messages = JavaValidation.line_messages
            vid = view.id()
            lineno = view.rowcol(view.sel()[0].end())[0] + 1
            if vid in line_messages and lineno in line_messages[vid]:
                view.set_status(
                    'subclim', '; '.join([e['message'] for e in line_messages[vid][lineno]]))
            else:
                view.erase_status('subclim')


class JavaImportClassUnderCursor(sublime_plugin.TextCommand):
    '''Will try to find a suitable class for importing using
    Eclipse's auto import features. Displays a menu if there are
    alternatives.'''

    def run(self, edit, block=False):
        if not check_eclim(self.view):
            return
        project, _file = get_context(self.view)
        pos = self.view.sel()[0]
        word = self.view.word(pos)
        offset = offset_of_location(self.view, word.a)
        self.view.run_command("save")

        class_names = []
        message = []

        def async_find_imports_task():
            import_result = self.call_eclim(project, _file, offset)
            if isinstance(import_result, list):
                class_names.extend(import_result)
            elif isinstance(import_result, dict):
                message.append(import_result['message'])
            elif isinstance(import_result, str):
                message.append(import_result)
            sublime.set_timeout(on_find_imports_finished, 0)

        def on_find_imports_finished():
            if len(message) > 0:
                log.error('\n'.join(message))
                return
            elif len(class_names) > 1:
                self.possible_imports = class_names
                self.show_import_menu()

        tasks.put(async_find_imports_task)

    def call_eclim(self, project, _file, offset):
        eclim.update_java_src(project, _file)
        complete_cmd = "-command java_import \
                                -p %s \
                                -f %s \
                                -o %i \
                                -e utf-8" % (project, _file, offset)
        result = eclim.call_eclim(complete_cmd)
        try:
            result = json.loads(result)
        except ValueError:
            pass
        return result

    def show_import_menu(self):
        self.view.window().show_quick_panel(
            self.possible_imports, self.import_selected,
            sublime.MONOSPACE_FONT)

    def import_selected(self, selected_idx):
        self.view.run_command("java_add_import_class",
                              {'class_name': self.possible_imports[selected_idx]})


class JavaAddImportClass(sublime_plugin.TextCommand):
    '''Will try to add a import statement to the current view.'''

    def run(self, edit, class_name=None):
        import_string = "import " + class_name + ";\n"
        lines = self.view.lines(sublime.Region(0, self.view.size()))
        last_import_region = sublime.Region(-1, -1)
        package_definition = sublime.Region(-1, -1)
        for l in lines:
            l_str = self.view.substr(l)
            if "{" in l_str:
                break
            if "package" in l_str:
                package_definition = l
            if "import" in l_str:
                last_import_region = l

        if last_import_region == sublime.Region(-1, -1):
            last_import_region = package_definition
            import_string = "\n" + import_string
        self.view.insert(edit, last_import_region.b + 1, import_string)


class EclipseProjects(sublime_plugin.WindowCommand):
    '''Open an eclipse project'''
    def __init__(self, *args, **kwargs):
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)
        self.projects = {}
        self.project_paths = []

    def run(self):
        if not check_eclim(self.window.active_view()):
            return
        self.projects = {}
        self.project_paths = []
        cmd = "-command projects"
        out = eclim.call_eclim(cmd)
        ps = json.loads(out.strip())
        for p in ps:
            self.projects[p['name']] = p
            self.project_paths.append([p['name'], p['path']])
        self.window.show_quick_panel(self.project_paths, self.on_done)

    def on_done(self, idx):
        name, path = self.project_paths[idx]
        branch, leaf = os.path.split(path)
        # open in finder
        self.window.run_command("open_dir", {"dir": branch, "file": leaf})
        # none of these work.
        # self.window.open_file(path)
        # self.window.run_command("prompt_add_folder", {"dir": path} )
        # self.window.run_command("prompt_add_folder", {"file": path} )
        # self.window.run_command("prompt_add_folder", path)
