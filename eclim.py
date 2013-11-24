'''
This module manages the connection to the Eclim server. It is responsible
for sending the commands and parsing the responses of the server.
It should be independent of any Sublime Text 2 API.

There is one global variable 'eclim_executable' that needs to be set before
using the module. It should point to the "eclim" executable in your Eclipse
directory.
'''
import os
import json
import subprocess
try:
    # Python 3
    from . import subclim_logging
except (ValueError):
    # Python 2
    import subclim_logging

try:
    unicode
except NameError:
    # Python 3
    basestring = str

# points to eclim executable, see module-level comments
eclim_executable = None

log = subclim_logging.getLogger('subclim')


class EclimExecutionException(Exception):
    pass


class NotInEclipseProjectException(Exception):
    pass


def call_eclim(cmdline):
    ''' Generic call to eclim including error-handling '''
    def arg_string(s):
        return "%s %s" % (eclim_executable, s)

    def arg_seq(args):
        a = [eclim_executable]
        a.extend(args)
        return a

    cmd = None
    shell = None
    if isinstance(cmdline, basestring):
        cmd = arg_string(cmdline)
        shell = True
    elif hasattr(cmdline, '__iter__'):
        cmd = arg_seq(cmdline)
        shell = False
    else:
        raise EclimExecutionException('Unknown command line passed. ' + repr(cmd) + ' ' + (type(cmd)))
    log.info('Run: %s', cmd)

    # running with shell=False spawns new command windows for
    # each execution of eclim_executable
    sinfo = None
    if os.name == 'nt' and not shell:
        sinfo = subprocess.STARTUPINFO()
        sinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        sinfo.wShowWindow = subprocess.SW_HIDE

    popen = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, startupinfo=sinfo)
    out, err = popen.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    log.debug("Results:\n" + out)

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
        raise EclimExecutionException(error_msg)
    return out


def get_context(filename):
    project_path = find_project_dir(filename)
    if not project_path:
        return None, None

    project_path = os.path.abspath(project_path)
    cmd = '-command project_list'
    out = call_eclim(cmd)
    if not out:
        return None, None

    try:
        obj = json.loads(out)
        for item in obj:
            path = os.path.abspath(item['path'])
            if path == project_path:
                relative = os.path.relpath(filename, project_path)
                return item['name'], relative
    except ValueError:
        subclim_logging.show_error_msg("Could not parse Eclim's response. "
                                       "Are you running Eclim version 1.7.3 or greater?")
    return None, None


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


def update_java_src(project, filename):
    '''Updates Eclipse's status regarding the given file.'''
    update_cmd = ['-command', 'java_src_update', '-p', project, '-f', filename, '-v']
    out = call_eclim(update_cmd)
    return out


def update_scala_src(project, filename):
    '''Updates Eclipse's status regarding the given file.'''
    update_cmd = ['-command', 'scala_src_update', '-p', project, '-f', filename, '-v']
    out = call_eclim(update_cmd)
    return out


def get_problems(project):
    ''' returns a list of problems that Eclipse found in the given project'''
    get_problems_cmd = ['-command', 'problems', '-p', project]
    out = call_eclim(get_problems_cmd)
    return out


def parse_problems(out):
    '''Turns a problem message into a nice dict-representation'''
    results = {"errors": []}
    try:
        obj = json.loads(out)
        for item in obj:
            filename = os.path.split(item['filename'])[1]
            isError = not item['warning']
            results["errors"].append({"file": filename, "line": item['line'], "message": item['message'], "filepath": item['filename'], "error": isError})
    except Exception as e:
        log.error(e)
        results["errors"].append({"eclim_exception": str(e)})
    return results
