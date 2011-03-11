import sublime_plugin, sublime
import eclim
import re, os

def match(rex, str):
    m = rex.match(str)
    if m:
        return m.group(0)
    else:
        return None

class SetEclimPath(sublime_plugin.WindowCommand):

    def run(self):
        win = self.window
        win.show_input_panel("Input path to eclim executable (in your eclipse directory)", 
            "/path/to/your/eclipse/eclim", self.entered_path, None, None)

    def entered_path(self, path):
        path = os.path.abspath(os.path.expanduser(path))
        s = sublime.load_settings("Eclim.sublime-settings")
        s.set("eclim_executable_location",path)
        sublime.save_settings("Eclim.sublime-settings")

class CompletionProposal(object):
    def __init__(self, name, insert=None, type="None"):
        self.name = name
        self.display = name
        if insert:
            self.insert = insert
        else:
            self.insert = name
        self.type = "None"

class JavaEclimCompletions(sublime_plugin.EventListener):

    def __init__(self):
        s = sublime.load_settings("Eclim.sublime-settings")
        eclim_executable = s.get("eclim_executable_location", None)
        eclim.set_executable(eclim_executable)

    def on_query_completions(self, view, prefix, locations):
        if not eclim.eclim_executable:
            print "you need to set the path to your eclim executable (command: set_eclim_path)"
            return []
        
        # we need to save the view on every call to completion, or eclipse
        # wont see the changes
        view.run_command("save")

        project, file = eclim.get_context(view)    
        pos = locations[0]

        if not view.match_selector(locations[0], "source.java"):
            return []

        proposals, with_snippets = self.to_proposals(self.call_eclim(project, file, pos))
        return [(p.display, p.insert) for p in proposals]

    def call_eclim(self, project, file, offset, shell=True):
        eclim.update_java_src(project, file)
        complete_cmd = "%s -command java_complete \
                                -p %s \
                                -f %s \
                                -o %i \
                                -e utf-8 \
                                -l compact" % (eclim.eclim_executable, 
                                                project, file, offset)
        out = eclim.call_eclim(complete_cmd)
        return out

    def to_proposals(self, eclim_output):
        results = [] 
        with_snippets = False
        for l in eclim_output.split("\n"):
            if not l: continue
            parts = l.split("|")

            if parts[1]:
                prop = CompletionProposal(parts[1])
                results.append(prop)
            else:
                variants = parts[3].split("<br/>")
                param_lists = [re.search(r'\((.*)\)', v).group(1) for v in variants]
                props = []
                for idx, pl in enumerate(param_lists):
                    params = [par.split(" ")[-1] for par in pl.split(", ")]
                    insert = ", ".join(["${%i:%s}" % (i,s) 
                                        for i,s in 
                                        zip(range(1,len(params)+1), params)
                                        ])
                    props.append(CompletionProposal(variants[idx], insert))
                    with_snippets = True
                results.extend(props)
            
        return results, with_snippets

class JavaValidation(sublime_plugin.EventListener):

    drawType = 4 | 32
    line_messages = {}

    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)
        self.lastCount = {}
        s = sublime.load_settings("Eclim.sublime-settings")
        eclim_executable = s.get("eclim_executable_location", None)
        eclim.set_executable(eclim_executable)

    def on_load(self, view):
        if "Java" in view.settings().get("syntax"):
            self.validate(view)

    def on_post_save(self, view):
        if "Java" in view.settings().get("syntax"):
            self.validate(view)

            def validation_closure():
                self.validate(view)
            sublime.set_timeout(validation_closure, 1500)

    def validate(self, view):
        line_messages = JavaValidation.line_messages
        project, file = eclim.get_context(view)    
        out = eclim.update_java_src(project, file)
        problems = self.problems_to_dict(out)
        vid = view.id()
        line_messages[vid] = {}
        for e in problems['errors']:
            l_no = int(e['line'])
            if not line_messages[vid].get(l_no,None):
                line_messages[vid][l_no] = []
            line_messages[vid][l_no].append(e['message'])
        self.visualize(view)
    
    def visualize(self, view):
        view.erase_regions('subclim-outlines')
        lines = JavaValidation.line_messages[view.id()].keys()

        outlines = [view.full_line(view.text_point(lineno-1, 0)) for lineno in lines]
        view.add_regions('subclim-outlines', outlines, 'keyword', JavaValidation.drawType)

    def problems_to_dict(self, problems):
        results = {"errors":[]}
        for pr in problems.split("\n"):
            if not pr: continue
            parts = pr.split("|")
            _file = os.path.split(parts[0])[1]
            filepath = parts[0]
            line = parts[1].split(" col ")[0]
            message = parts[2]
            results["errors"].append({"file":_file, "line":line,
                                    "message":message, "filepath":filepath})
        return results

    def on_selection_modified(self, view):
        if "Java" in view.settings().get("syntax"):
            line_messages = JavaValidation.line_messages
            vid = view.id()
            lineno = view.rowcol(view.sel()[0].end())[0]+1
            if vid in line_messages and lineno in line_messages[vid]:
                view.set_status('subclim', '; '.join(line_messages[vid][lineno]))
            else:
                view.erase_status('subclim')