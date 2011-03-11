#!/usr/bin/env python
import sys, os, subprocess
from xml.etree import ElementTree

class NotInEclipseProjectException(Exception):
    pass

eclim_executable = None

def set_executable(eclim_exec):
    global eclim_executable
    eclim_executable = eclim_exec

def call_eclim(cmd):
    popen = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    out, err = popen.communicate()
    if err or "Connection refused" in out:
        error_msg = 'Error connecting to Eclim server: '
        if out: error_msg += out
        if err: error_msg += err
        if "Connection refused" in out:
            error_msg += " Is Eclipse running?"
        raise Exception(error_msg)
    return out

def get_context(view):
    file_path = view.file_name()
    project_dir = find_project_dir(file_path)
    project, file = None, None
    
    if project_dir:
        project_file = os.path.join(project_dir, '.project')
        if not os.path.isfile(project_file):
            # if no project file is found, we are not in
            # an eclipse java project -> die silently
            raise NotInEclipseProjectException()
        with open(project_file) as pf:
            project_desc = ElementTree.XML(pf.read())
        project = project_desc.find('name').text
        file = os.path.relpath(file_path, project_dir)
        
    return project, file

def find_project_dir(file_dir):
    def traverse_upward(look_for, start_at="."):
        p = os.path.abspath(start_at)

        while True:
            if look_for in os.listdir(p):
                return p
            new_p =  os.path.abspath(os.path.join(p, ".."))
            if new_p == p:
                return None
            p = new_p

    return traverse_upward(".project", start_at=os.path.split(file_dir)[0])

def update_java_src(project, file):
    global eclim_executable
    update_cmd = '%s -command java_src_update \
                        -p %s \
                        -f %s \
                        -v' % (eclim_executable, project, file)
    out = call_eclim(update_cmd)
    return out

def refresh_file(project, file):
    global eclim_executable
    refresh_cmd = '%s -command project_refresh_file \
                        -p %s \
                        -f %s ' % (eclim_executable, project, file)
    out = call_eclim(refresh_cmd)
    return out

def get_problems(project):
    global eclim_executable
    get_problems_cmd = '%s -command problems \
                        -p %s' % (eclim_executable, project)
    out = call_eclim(get_problems_cmd)
    return out
    
def format_problems(problems):
    result = ""
    for pr in problems.split("\n"):
        if not pr: continue
        parts = pr.split("|")
        result += parts[1].replace(" col ",":")+" "
        result += parts[2]
    return result

def problems_to_dict(problems):
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

# def close_error_window(window_token):
#     cmd = DIALOG + " -x "+window_token
#     popen = subprocess.Popen(
#         cmd, stdin=None, stdout=None,shell=True)
#     popen.communicate()

# def show_error_window(problems):
#     ''' prints out the window token returned by tm_dialog to the 
#     calling TM command (or -1 indicating failure)'''
#     if not problems['errors']:
#         print "-1"
#         return
#     path = os.path.join(os.path.dirname(sys.argv[0]), "build_errors.nib")
#     cmd = DIALOG + ' -a "%s"' % path
#     popen = subprocess.Popen(
#         cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
#     out, err = popen.communicate(plistlib.writePlistToString(problems))
#     print out
    
# def update_error_window(window_token, problems):
#     # if not problems['errors']:
#     #    close_error_window(window_token)
#     # else:
#     cmd = DIALOG + " -t "+window_token
#     popen = subprocess.Popen(
#         cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
#     out, err = popen.communicate(plistlib.writePlistToString(problems))

# def show_markers(problems):
#     tm = app('TextMate')
#     tm.clear_marker()

#     filepath = os.environ['TM_FILEPATH']
#     problems = filter(lambda p: p['filepath']==filepath, problems["errors"])
#     for p in problems:
#         tm.add_marker(p['line'])

# def display_problems(problems):
#     cmd = DIALOG + " -l"
#     popen = subprocess.Popen(
#         cmd, stdin=None, stdout=subprocess.PIPE,shell=True)
#     out, err = popen.communicate()
#     if JAVA_BUILD_ERRORS_WINDOW in out:
#         windows = out.splitlines()
#         for w in windows:
#             m1 = re.match(r'(\d*) \((.*)\)',w)
#             if m1.group(2) == JAVA_BUILD_ERRORS_WINDOW:
#                 token = m1.group(1)
#         update_error_window(token, problems)
#     else:
#         show_error_window(problems)
    
#     #show_markers(problems)

if __name__ == '__main__':
    try:
        if sys.argv[1] == '--update':
            project, file = get_context()
            problems = update_java_src(project, file)
            #tooltip(problems)
            refresh_file(project, file)
            # display_problems(problems_to_dict(problems))
    except NotInEclipseProjectException, e:
        # die silently
        print "-1"
    except Exception, e:
        tooltip(str(e))
        print "-1"