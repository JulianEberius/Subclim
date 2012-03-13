'''
This module manages the connection to the Eclim server. It is responsible
for sending the commands and parsing the responses of the server.
It should be independent of any Sublime Text 2 API.

There is one global variable 'eclim_executable' that needs to be set before
using the module. It should point to the "eclim" executable in your Eclipse
directory.
'''
import re
import os
import subprocess
from sublime_logging import *
from xml.etree import ElementTree
try:
    # ST2 does not always bundle expat (e.g. not on Linux)
    from xml.parsers import expat
except ImportError:
    from elementtree import SimpleXMLTreeBuilder
    ElementTree.XMLTreeBuilder = SimpleXMLTreeBuilder.TreeBuilder

# points to eclim executable, see module-level comments
eclim_executable = None

log = getLogger('subclim')

class NotInEclipseProjectException(Exception):
    pass

def call_eclim(cmd):
    ''' Generic call to eclim including error-handling '''
    cmd = "%s %s" % (eclim_executable, cmd)
    log.debug('run: ' + re.sub("  +", " ", cmd))
    popen = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = popen.communicate()

    # error handling
    if err or "Connection refused" in out:
        error_msg = 'Error connecting to Eclim server: '
        if out:
            error_msg += out
        if err:
            error_msg += err
        if "Connection refused" in out:
            error_msg += " Is Eclipse running?"
        log.error(error_msg)
        raise Exception(error_msg)
    return out

def get_context(file_path):
    ''' Given an absolute file_path (e.g. as returned by ST2's
    view.file_path()) it returns the Eclipse project name and file path
    relative to the project root. It looks for the '.project' file that
    Eclipse creates to do this.
    '''
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
        try:
            project = project_desc.find('name').text
            file = os.path.relpath(file_path, project_dir)
        except Exception, e:
            raise Exception("Could not parse project file: %s.\nException: %s"
                % (project_file, e))

    return project, file


def find_project_dir(file_dir):
    ''' tries to find a '.project' file as created by Eclipse to mark
    project folders by traversing the directory tree upward from the given
    directory'''
    def traverse_upward(look_for, start_at="."):
        p = os.path.abspath(start_at)

        while True:
            if look_for in os.listdir(p):
                return p
            new_p = os.path.abspath(os.path.join(p, ".."))
            if new_p == p:
                return None
            p = new_p

    if os.path.isfile(file_dir):
        file_dir = os.path.dirname(file_dir)
    return traverse_upward(".project", start_at=file_dir)


def update_java_src(project, file):
    '''Updates Eclipse's status regarding the given file.
    I have forgotten what it actually does ;-)'''
    update_cmd = '-command java_src_update \
                    -p %s \
                    -f %s \
                    -v' % (project, file)
    out = call_eclim(update_cmd)
    return out


def get_problems(project):
    ''' returs a list of problems that Eclipse found in the given project'''
    get_problems_cmd = '-command problems \
                        -p %s' % (project)
    out = call_eclim(get_problems_cmd)
    return out


def parse_problems(problem_string):
    '''Turns a problem message into a nice dict-representation'''
    results = {"errors": []}
    try:
        for pr in problem_string.split("\n"):
            if not pr:
                continue
            print pr
            parts = pr.split("|")
            _file = os.path.split(parts[0])[1]
            filepath = parts[0]
            line = parts[1].split(" col ")[0]
            message = parts[2]
            isError = parts[3] == 'e'
            results["errors"].append({"file": _file, "line": line,
                                    "message": message, "filepath": filepath, "error": isError})
        return results
    except Exception, e:
        print e
        results["errors"].append({"eclim_exception": str(e)})
        return results
