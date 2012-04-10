#!/usr/bin/env python
'''Let's cheat and generate commands based off of what the help output claims.'''
import sys
import re
from pprint import pprint


remove = ('command', 'plugin', 'AbstractEclimApplication', 'admin')
substitute = {
    'pdt': 'Php',
    'wst': 'Web',
    'jdt': 'Java',
    'cdt': 'Clang',
    'dltk': 'Dynamic',
    'dltkruby': 'Ruby',
    'JavaCommand': 'RunCommand',
    'JavacCommand': 'CompileCommand'
}
packages = {
    'org.eclim.plugin.jdt': 'Java.tmLanguage'
    # more to follow
}


def pairs(items):
    '''magical.'''
    return zip(*[iter(items)] * 2)


def package_name(klass):
    for k in packages.keys():
        if klass.startswith(k):
            return packages[k]
    return None


def plugin_name(klass):
    '''org.eclim.plugin.toolkit.command.dostuff.DoStuffCommand => SubclimToolkitDoStuffCommand'''
    # it ain't perfect, but it'll get the job done
    klass = klass.replace('org.eclim.', '')

    # fancy capitalization
    s = [substitute.get(x, x[0].upper() + x[1:]) for x in klass.split('.') if x not in remove]
    # strip out the last part of the package if it's part of the name
    if s[-2] in s[-1]:
        del s[-2]
    return 'Subclim' + ''.join(s)


def command_name(plugin):
    plugin = re.sub('Command$', '', plugin)
    plugin = plugin[0] + re.sub('([A-Z])', '_\\1', plugin[1:])
    return plugin.lower()


def parse_args(command):
    '''Create a list of arguments from the command output'''
    def append(acc):
        if len(acc) > 0:
            ret[k].append(' '.join(acc))
        return []
    ret = {}
    items = command.split(' ')
    k = items[0]
    ret[k] = []
    acc = []
    for i in items[1:]:
        if i.startswith('-') or i.startswith('[-'):
            acc = append(acc)
        acc.append(i)
    append(acc)
    return ret


def main(args):
    lines = sys.stdin.readlines()
    print '#!/usr/bin/env python'
    print 'import sys, os, string, re, subprocess, sublime, sublime_plugin, subclim_logging'
    print 'from subclim_plugin import SubclimBase'
    print 'log = subclim_logging.getLogger("subclim")'
    print
    for command, klass in pairs(lines):
        klass = klass.strip().replace('class: ', '')
        command = command.strip()
        plugin = plugin_name(klass)
        package = package_name(klass)
        print '#', klass
        print '#', command
        print 'class', plugin + '(sublime_plugin.TextCommand, SubclimBase):'
        print '\ttemplate = ' + repr(parse_args(command))
        if package is not None:
            print '\tdef is_visible(self):'
            print '\t\treturn ' + repr(package) + ' in self.view.settings().get("syntax")'
        print '\tdef run(self, edit, **kwargs):'
        if package is not None:
            print '\t\tif not self.is_visible(): return'
        print '\t\tout = self.run_template(' + plugin + '.template, **kwargs)'
        print '\t\tlog.debug("Results:\\n" + out)'
        print

    sublime_commands = []
    for command, klass in pairs(lines):
        klass = klass.strip().replace('class: ', '')
        command = re.sub(' .*$', '', command.strip())
        sublime_commands.append({'caption': 'Subclim: ' + command, 'command': command_name(plugin_name(klass))})
    pprint(sublime_commands)

if __name__ == '__main__':
    main(sys.argv[1:])
