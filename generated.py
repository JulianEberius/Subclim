#!/usr/bin/env python
import sublime_plugin
try:
    # Python 3
    from . import subclim_logging
    from .subclim_plugin import SubclimBase
except (ValueError):
    # Python 2
    import subclim_logging
    from subclim_plugin import SubclimBase

log = subclim_logging.getLogger("subclim")


class SubclimJavaSrcCompileCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.src.JavacCommand
    javac -p project'''
    template = {'javac': ['-p project']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSrcCompileCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaClasspathVariableDeleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.classpath.ClasspathVariableDeleteCommand
    java_classpath_variable_delete -n name'''
    template = {'java_classpath_variable_delete': ['-n name']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaClasspathVariableDeleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaRefactoringUndoCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.refactoring.UndoCommand
    java_refactor_undo [-p]'''
    template = {'java_refactor_undo': ['[-p]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaRefactoringUndoCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaSrcClassPrototypeCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.src.ClassPrototypeCommand
    java_class_prototype -c classname [-p project] [-f file]'''
    template = {'java_class_prototype': ['-c classname', '[-p project]', '[-f file]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSrcClassPrototypeCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaImplCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.impl.ImplCommand
    java_impl -p project -f file [-o offset] [-e encoding] [-t type] [-s superType] [-m methods]'''
    template = {'java_impl': ['-p project', '-f file', '[-o offset]', '[-e encoding]', '[-t type]', '[-s superType]', '[-m methods]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaImplCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaLog4jValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.log4j.ValidateCommand
    log4j_validate -p project -f file'''
    template = {'log4j_validate': ['-p project', '-f file']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaLog4jValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaConstructorCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.constructor.ConstructorCommand
    java_constructor -p project -f file -o offset [-e encoding] [-r properties]'''
    template = {'java_constructor': ['-p project', '-f file', '-o offset', '[-e encoding]', '[-r properties]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaConstructorCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaDocJavadocCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.doc.JavadocCommand
    javadoc -p project [-f file]'''
    template = {'javadoc': ['-p project', '[-f file]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaDocJavadocCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaBeanPropertiesCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.bean.PropertiesCommand
    java_bean_properties -p project -f file -o offset [-e encoding] -r properties -t type [-i]'''
    template = {'java_bean_properties': ['-p project', '-f file', '-o offset', '[-e encoding]', '-r properties', '-t type', '[-i]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaBeanPropertiesCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaDocSearchCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.doc.DocSearchCommand
    java_docsearch -n project [-f file] [-o offset] [-e encoding] [-l length] [-p pattern] [-t type] [-x context] [-s scope]'''
    template = {'java_docsearch': ['-n project', '[-f file]', '[-o offset]', '[-e encoding]', '[-l length]', '[-p pattern]', '[-t type]', '[-x context]', '[-s scope]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaDocSearchCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaIncludeImportOrderCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.include.ImportOrderCommand
    java_import_order -p project'''
    template = {'java_import_order': ['-p project']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaIncludeImportOrderCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaSrcDirsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.src.SrcDirsCommand
    java_src_dirs -p project'''
    template = {'java_src_dirs': ['-p project']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSrcDirsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaSrcFindCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.src.SrcFindCommand
    java_src_find -c classname [-p project]'''
    template = {'java_src_find': ['-c classname', '[-p project]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSrcFindCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaHierarchyCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.hierarchy.HierarchyCommand
    java_hierarchy -p project -f file -o offset -e encoding'''
    template = {'java_hierarchy': ['-p project', '-f file', '-o offset', '-e encoding']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaHierarchyCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaLaunchingListVmInstalls(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.launching.ListVmInstalls
    java_list_installs'''
    template = {'java_list_installs': []}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaLaunchingListVmInstalls.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaIncludeImportCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.include.ImportCommand
    java_import -n project -p pattern [-t type]'''
    template = {'java_import': ['-n project', '-p pattern', '[-t type]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaIncludeImportCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaRefactoringRenameCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.refactoring.RenameCommand
    java_refactor_rename -p project -f file -n name -o offset -l length -e encoding [-v] [-d diff]'''
    template = {'java_refactor_rename': ['-p project', '-f file', '-n name', '-o offset', '-l length', '-e encoding', '[-v]', '[-d diff]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaRefactoringRenameCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaRefactoringRedoCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.refactoring.RedoCommand
    java_refactor_redo [-p]'''
    template = {'java_refactor_redo': ['[-p]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaRefactoringRedoCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaCodeCorrectCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.correct.CodeCorrectCommand
    java_correct -p project -f file -l line -o offset [-e encoding] [-a apply]'''
    template = {'java_correct': ['-p project', '-f file', '-l line', '-o offset', '[-e encoding]', '[-a apply]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaCodeCorrectCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaClasspathVariablesCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.classpath.ClasspathVariablesCommand
    java_classpath_variables'''
    template = {'java_classpath_variables': []}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaClasspathVariablesCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaWebxmlValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.webxml.ValidateCommand
    webxml_validate -p project -f file'''
    template = {'webxml_validate': ['-p project', '-f file']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaWebxmlValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaDelegateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.delegate.DelegateCommand
    java_delegate -p project -f file -o offset -e encoding [-t type] [-s superType] [-m methods]'''
    template = {'java_delegate': ['-p project', '-f file', '-o offset', '-e encoding', '[-t type]', '[-s superType]', '[-m methods]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaDelegateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaIncludeImportMissingCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.include.ImportMissingCommand
    java_import_missing -p project -f file'''
    template = {'java_import_missing': ['-p project', '-f file']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaIncludeImportMissingCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaDocCommentCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.doc.CommentCommand
    javadoc_comment -p project -f file -o offset [-e encoding]'''
    template = {'javadoc_comment': ['-p project', '-f file', '-o offset', '[-e encoding]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaDocCommentCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.complete.CodeCompleteCommand
    java_complete -p project -f file -o offset -e encoding -l layout'''
    template = {'java_complete': ['-p project', '-f file', '-o offset', '-e encoding', '-l layout']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaSrcUpdateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.src.SrcUpdateCommand
    java_src_update -p project -f file [-v] [-b]'''
    template = {'java_src_update': ['-p project', '-f file', '[-v]', '[-b]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSrcUpdateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaCheckstyleCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.checkstyle.CheckstyleCommand
    java_checkstyle -p project -f file'''
    template = {'java_checkstyle': ['-p project', '-f file']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaCheckstyleCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaIncludeUnusedImportsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.include.UnusedImportsCommand
    java_imports_unused -p project -f file'''
    template = {'java_imports_unused': ['-p project', '-f file']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaIncludeUnusedImportsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaClasspathCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.classpath.ClasspathCommand
    java_classpath -p project [-d delimiter]'''
    template = {'java_classpath': ['-p project', '[-d delimiter]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaClasspathCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaFormatCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.format.FormatCommand
    java_format -p project -f file -b boffset -e eoffset'''
    template = {'java_format': ['-p project', '-f file', '-b boffset', '-e eoffset']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaFormatCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaClasspathVariableCreateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.classpath.ClasspathVariableCreateCommand
    java_classpath_variable_create -n name -p path'''
    template = {'java_classpath_variable_create': ['-n name', '-p path']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaClasspathVariableCreateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaJunitJUnitImplCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.junit.JUnitImplCommand
    java_junit_impl -p project -f file [-o offset] [-e encoding] [-t type] [-b baseType] [-s superType] [-m methods]'''
    template = {'java_junit_impl': ['-p project', '-f file', '[-o offset]', '[-e encoding]', '[-t type]', '[-b baseType]', '[-s superType]', '[-m methods]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaJunitJUnitImplCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimAntRunTargetsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.ant.command.run.TargetsCommand
    ant_targets -p project -f file'''
    template = {'ant_targets': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimAntRunTargetsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaSrcFileExistsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.src.SrcFileExistsCommand
    java_src_exists -f file [-p project]'''
    template = {'java_src_exists': ['-f file', '[-p project]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSrcFileExistsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimAntCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.ant.command.complete.CodeCompleteCommand
    ant_complete -p project -f file -o offset -e encoding'''
    template = {'ant_complete': ['-p project', '-f file', '-o offset', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimAntCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaSrcRunCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.src.JavaCommand
    java -p project [-d] [-c classname] [-w workingdir] [-v vmargs] [-s sysprops] [-e envargs] [-a args]'''
    template = {'java': ['-p project', '[-d]', '[-c classname]', '[-w workingdir]', '[-v vmargs]', '[-s sysprops]', '[-e envargs]', '[-a args]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSrcRunCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimMavenDependencySearchCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.maven.command.dependency.SearchCommand
    maven_dependency_search -p project -f file -t type -s search'''
    template = {'maven_dependency_search': ['-p project', '-f file', '-t type', '-s search']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimMavenDependencySearchCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimAntValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.ant.command.validate.ValidateCommand
    ant_validate -p project -f file'''
    template = {'ant_validate': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimAntValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimJavaSearchCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.jdt.command.search.SearchCommand
    java_search [-n project] [-f file] [-o offset] [-e encoding] [-l length] [-p pattern] [-t type] [-x context] [-s scope] [-i]'''
    template = {'java_search': ['[-n project]', '[-f file]', '[-o offset]', '[-e encoding]', '[-l length]', '[-p pattern]', '[-t type]', '[-x context]', '[-s scope]', '[-i]']}

    def is_visible(self):
        return 'Java.tmLanguage' in self.view.settings().get("syntax")

    def run(self, edit, **kwargs):
        if not self.is_visible():
            return
        out = self.run_template(SubclimJavaSearchCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimEclipseReloadCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.eclipse.AbstractEclimApplication.ReloadCommand
    reload'''
    template = {'reload': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimEclipseReloadCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreArchiveReadCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.archive.ArchiveReadCommand
    archive_read -f file'''
    template = {'archive_read': ['-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreArchiveReadCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreEclipseJobsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.eclipse.JobsCommand
    jobs [-f family]'''
    template = {'jobs': ['[-f family]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreEclipseJobsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectBuildCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectBuildCommand
    project_build -p project'''
    template = {'project_build': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectBuildCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreSearchLocateFileCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.search.LocateFileCommand
    locate_file -p pattern -s scope [-n project] [-f file]'''
    template = {'locate_file': ['-p pattern', '-s scope', '[-n project]', '[-f file]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreSearchLocateFileCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreSettingsUpdateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.admin.SettingsUpdateCommand
    settings_update [-s settings]'''
    template = {'settings_update': ['[-s settings]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreSettingsUpdateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectDeleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectDeleteCommand
    project_delete -p project'''
    template = {'project_delete': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectDeleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreSettingsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.admin.SettingsCommand
    settings'''
    template = {'settings': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreSettingsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectMoveCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectMoveCommand
    project_move -p project -d dir'''
    template = {'project_move': ['-p project', '-d dir']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectMoveCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreXmlValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.xml.ValidateCommand
    xml_validate -p project -f file [-s]'''
    template = {'xml_validate': ['-p project', '-f file', '[-s]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreXmlValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreEclipseWorkspaceCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.eclipse.WorkspaceCommand
    workspace_dir'''
    template = {'workspace_dir': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreEclipseWorkspaceCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreHistoryRevisionCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.history.HistoryRevisionCommand
    history_revision -p project -f file -r revision'''
    template = {'history_revision': ['-p project', '-f file', '-r revision']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreHistoryRevisionCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectNatureAliasesCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectNatureAliasesCommand
    project_nature_aliases'''
    template = {'project_nature_aliases': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectNatureAliasesCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectUpdateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectUpdateCommand
    project_update -p project [-b buildfile] [-s settings]'''
    template = {'project_update': ['-p project', '[-b buildfile]', '[-s settings]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectUpdateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectOpenCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectOpenCommand
    project_open -p project'''
    template = {'project_open': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectOpenCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectCreateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectCreateCommand
    project_create -f folder [-p name] -n natures [-d depends]'''
    template = {'project_create': ['-f folder', '[-p name]', '-n natures', '[-d depends]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectCreateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectRefreshCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectRefreshCommand
    project_refresh -p project'''
    template = {'project_refresh': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectRefreshCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCorePingCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.admin.PingCommand
    ping'''
    template = {'ping': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCorePingCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectSettingCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectSettingCommand
    project_setting -p project -s setting [-v value]'''
    template = {'project_setting': ['-p project', '-s setting', '[-v value]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectSettingCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreShutdownCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.admin.ShutdownCommand
    shutdown'''
    template = {'shutdown': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreShutdownCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreHistoryClearCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.history.HistoryClearCommand
    history_clear -p project -f file'''
    template = {'history_clear': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreHistoryClearCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreXmlFormatCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.xml.FormatCommand
    xml_format -f file -w linewidth -i indent -m fileformat'''
    template = {'xml_format': ['-f file', '-w linewidth', '-i indent', '-m fileformat']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreXmlFormatCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProblemsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.problems.ProblemsCommand
    problems -p project [-e]'''
    template = {'problems': ['-p project', '[-e]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProblemsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectSettingsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectSettingsCommand
    project_settings [-p project]'''
    template = {'project_settings': ['[-p project]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectSettingsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectNatureAddCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectNatureAddCommand
    project_nature_add -p project -n nature'''
    template = {'project_nature_add': ['-p project', '-n nature']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectNatureAddCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectByResource(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectByResource
    project_by_resource -f file'''
    template = {'project_by_resource': ['-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectByResource.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectLinkResource(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectLinkResource
    project_link_resource -f file'''
    template = {'project_link_resource': ['-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectLinkResource.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreHistoryListCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.history.HistoryListCommand
    history_list -p project -f file'''
    template = {'history_list': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreHistoryListCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectCloseCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectCloseCommand
    project_close -p project'''
    template = {'project_close': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectCloseCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreHistoryAddCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.history.HistoryAddCommand
    history_add -p project -f file'''
    template = {'history_add': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreHistoryAddCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectsCommand
    projects'''
    template = {'projects': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectInfoCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectInfoCommand
    project_info -p project'''
    template = {'project_info': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectInfoCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectListCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectListCommand
    project_list [-n nature]'''
    template = {'project_list': ['[-n nature]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectListCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectNaturesCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectNaturesCommand
    project_natures [-p project]'''
    template = {'project_natures': ['[-p project]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectNaturesCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectRefreshFileCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectRefreshFileCommand
    project_refresh_file -p project -f file'''
    template = {'project_refresh_file': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectRefreshFileCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectImportCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectImportCommand
    project_import -f folder'''
    template = {'project_import': ['-f folder']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectImportCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectNatureRemoveCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectNatureRemoveCommand
    project_nature_remove -p project -n nature'''
    template = {'project_nature_remove': ['-p project', '-n nature']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectNatureRemoveCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimCoreProjectRenameCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.core.command.project.ProjectRenameCommand
    project_rename -p project -n name'''
    template = {'project_rename': ['-p project', '-n name']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimCoreProjectRenameCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicBuildpathsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.buildpath.BuildpathsCommand
    dltk_buildpaths -p project'''
    template = {'dltk_buildpaths': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicBuildpathsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicBuildpathVariableCreateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.buildpath.BuildpathVariableCreateCommand
    dltk_buildpath_variable_create -n name -p path'''
    template = {'dltk_buildpath_variable_create': ['-n name', '-p path']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicBuildpathVariableCreateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicLaunchingInterpretersCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.launching.InterpretersCommand
    dltk_interpreters [-p project] [-n nature]'''
    template = {'dltk_interpreters': ['[-p project]', '[-n nature]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicLaunchingInterpretersCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicLaunchingDeleteInterpreterCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.launching.DeleteInterpreterCommand
    dltk_remove_interpreter -n nature -i interpreter'''
    template = {'dltk_remove_interpreter': ['-n nature', '-i interpreter']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicLaunchingDeleteInterpreterCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicBuildpathVariableDeleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.buildpath.BuildpathVariableDeleteCommand
    dltk_buildpath_variable_delete -n name'''
    template = {'dltk_buildpath_variable_delete': ['-n name']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicBuildpathVariableDeleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicSearchCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.search.SearchCommand
    dltk_search [-n project] [-f file] [-o offset] [-l length] [-e encoding] [-p pattern] [-t type] [-x context] [-s scope] [-i]'''
    template = {'dltk_search': ['[-n project]', '[-f file]', '[-o offset]', '[-l length]', '[-e encoding]', '[-p pattern]', '[-t type]', '[-x context]', '[-s scope]', '[-i]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicSearchCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicLaunchingAddInterpreterCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.launching.AddInterpreterCommand
    dltk_add_interpreter -n nature -t type -i interpreter'''
    template = {'dltk_add_interpreter': ['-n nature', '-t type', '-i interpreter']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicLaunchingAddInterpreterCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimDynamicBuildpathVariablesCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltk.command.buildpath.BuildpathVariablesCommand
    dltk_buildpath_variables'''
    template = {'dltk_buildpath_variables': []}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimDynamicBuildpathVariablesCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimPhpSrcUpdateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.pdt.command.src.SrcUpdateCommand
    php_src_update -p project -f file [-v] [-b]'''
    template = {'php_src_update': ['-p project', '-f file', '[-v]', '[-b]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimPhpSrcUpdateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimPhpCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.pdt.command.complete.CodeCompleteCommand
    php_complete -p project -f file -o offset -e encoding'''
    template = {'php_complete': ['-p project', '-f file', '-o offset', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimPhpCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimPhpSearchCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.pdt.command.search.SearchCommand
    php_search [-n project] [-f file] [-o offset] [-l length] [-e encoding] [-p pattern] [-t type] [-x context] [-s scope] [-i]'''
    template = {'php_search': ['[-n project]', '[-f file]', '[-o offset]', '[-l length]', '[-e encoding]', '[-p pattern]', '[-t type]', '[-x context]', '[-s scope]', '[-i]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimPhpSearchCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangSrcUpdateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.src.SrcUpdateCommand
    c_src_update -p project -f file [-v] [-b]'''
    template = {'c_src_update': ['-p project', '-f file', '[-v]', '[-b]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangSrcUpdateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangProjectSourceEntryCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.project.SourceEntryCommand
    c_project_src -p project -a action -d dir [-e excludes]'''
    template = {'c_project_src': ['-p project', '-a action', '-d dir', '[-e excludes]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangProjectSourceEntryCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangProjectSourcePathsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.project.SourcePathsCommand
    c_sourcepaths -p project'''
    template = {'c_sourcepaths': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangProjectSourcePathsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangProjectIncludePathsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.project.IncludePathsCommand
    c_includepaths -p project'''
    template = {'c_includepaths': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangProjectIncludePathsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangSearchCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.search.SearchCommand
    c_search [-n project] [-f file] [-o offset] [-l length] [-e encoding] [-p pattern] [-t type] [-x context] [-s scope] [-i]'''
    template = {'c_search': ['[-n project]', '[-f file]', '[-o offset]', '[-l length]', '[-e encoding]', '[-p pattern]', '[-t type]', '[-x context]', '[-s scope]', '[-i]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangSearchCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangProjectConfigurationsCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.project.ConfigurationsCommand
    c_project_configs -p project'''
    template = {'c_project_configs': ['-p project']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangProjectConfigurationsCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangProjectSymbolEntryCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.project.SymbolEntryCommand
    c_project_symbol -p project -a action -l lang -n name [-v value]'''
    template = {'c_project_symbol': ['-p project', '-a action', '-l lang', '-n name', '[-v value]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangProjectSymbolEntryCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangProjectIncludeEntryCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.project.IncludeEntryCommand
    c_project_include -p project -a action -l lang -d dir'''
    template = {'c_project_include': ['-p project', '-a action', '-l lang', '-d dir']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangProjectIncludeEntryCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangCallHierarchyCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.hierarchy.CallHierarchyCommand
    c_callhierarchy -p project -f file -o offset -l length -e encoding'''
    template = {'c_callhierarchy': ['-p project', '-f file', '-o offset', '-l length', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangCallHierarchyCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimClangCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.cdt.command.complete.CodeCompleteCommand
    c_complete -p project -f file -o offset -e encoding -l layout'''
    template = {'c_complete': ['-p project', '-f file', '-o offset', '-e encoding', '-l layout']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimClangCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebXsdValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.validate.XsdValidateCommand
    xsd_validate -p project -f file'''
    template = {'xsd_validate': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebXsdValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebHtmlCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.complete.HtmlCodeCompleteCommand
    html_complete -p project -f file -o offset -e encoding'''
    template = {'html_complete': ['-p project', '-f file', '-o offset', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebHtmlCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebHtmlValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.validate.HtmlValidateCommand
    html_validate -p project -f file'''
    template = {'html_validate': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebHtmlValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebJavaScriptCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.complete.JavaScriptCodeCompleteCommand
    javascript_complete -p project -f file -o offset -e encoding'''
    template = {'javascript_complete': ['-p project', '-f file', '-o offset', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebJavaScriptCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebCssValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.validate.CssValidateCommand
    css_validate -p project -f file'''
    template = {'css_validate': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebCssValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebJavaScriptSrcUpdateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.src.JavaScriptSrcUpdateCommand
    javascript_src_update -p project -f file [-v]'''
    template = {'javascript_src_update': ['-p project', '-f file', '[-v]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebJavaScriptSrcUpdateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebCssCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.complete.CssCodeCompleteCommand
    css_complete -p project -f file -o offset -e encoding'''
    template = {'css_complete': ['-p project', '-f file', '-o offset', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebCssCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebXmlCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.complete.XmlCodeCompleteCommand
    xml_complete -p project -f file -o offset -e encoding'''
    template = {'xml_complete': ['-p project', '-f file', '-o offset', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebXmlCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimWebDtdValidateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.wst.command.validate.DtdValidateCommand
    dtd_validate -p project -f file'''
    template = {'dtd_validate': ['-p project', '-f file']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimWebDtdValidateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimRubySrcUpdateCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltkruby.command.src.SrcUpdateCommand
    ruby_src_update -p project -f file [-v] [-b]'''
    template = {'ruby_src_update': ['-p project', '-f file', '[-v]', '[-b]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimRubySrcUpdateCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimRubyCodeCompleteCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltkruby.command.complete.CodeCompleteCommand
    ruby_complete -p project -f file -o offset -e encoding'''
    template = {'ruby_complete': ['-p project', '-f file', '-o offset', '-e encoding']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimRubyCodeCompleteCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimRubySearchCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltkruby.command.search.SearchCommand
    ruby_search [-n project] [-f file] [-o offset] [-l length] [-e encoding] [-p pattern] [-t type] [-x context] [-s scope] [-i]'''
    template = {'ruby_search': ['[-n project]', '[-f file]', '[-o offset]', '[-l length]', '[-e encoding]', '[-p pattern]', '[-t type]', '[-x context]', '[-s scope]', '[-i]']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimRubySearchCommand.template, **kwargs)
        log.debug("Results:\n" + out)


class SubclimRubyLaunchingAddInterpreterCommand(sublime_plugin.TextCommand, SubclimBase):
    '''org.eclim.plugin.dltkruby.command.launching.AddInterpreterCommand
    ruby_add_interpreter -n nature -i interpreter'''
    template = {'ruby_add_interpreter': ['-n nature', '-i interpreter']}

    def run(self, edit, **kwargs):
        out = self.run_template(SubclimRubyLaunchingAddInterpreterCommand.template, **kwargs)
        log.debug("Results:\n" + out)

'''
[{'caption': 'Subclim: javac', 'command': 'subclim_java_src_compile'},
 {'caption': 'Subclim: java_classpath_variable_delete',
  'command': 'subclim_java_classpath_variable_delete'},
 {'caption': 'Subclim: java_refactor_undo',
  'command': 'subclim_java_refactoring_undo'},
 {'caption': 'Subclim: java_class_prototype',
  'command': 'subclim_java_src_class_prototype'},
 {'caption': 'Subclim: java_impl', 'command': 'subclim_java_impl'},
 {'caption': 'Subclim: log4j_validate',
  'command': 'subclim_java_log4j_validate'},
 {'caption': 'Subclim: java_constructor',
  'command': 'subclim_java_constructor'},
 {'caption': 'Subclim: javadoc', 'command': 'subclim_java_doc_javadoc'},
 {'caption': 'Subclim: java_bean_properties',
  'command': 'subclim_java_bean_properties'},
 {'caption': 'Subclim: java_docsearch', 'command': 'subclim_java_doc_search'},
 {'caption': 'Subclim: java_import_order',
  'command': 'subclim_java_include_import_order'},
 {'caption': 'Subclim: java_src_dirs', 'command': 'subclim_java_src_dirs'},
 {'caption': 'Subclim: java_src_find', 'command': 'subclim_java_src_find'},
 {'caption': 'Subclim: java_hierarchy', 'command': 'subclim_java_hierarchy'},
 {'caption': 'Subclim: java_list_installs',
  'command': 'subclim_java_launching_list_vm_installs'},
 {'caption': 'Subclim: java_import', 'command': 'subclim_java_include_import'},
 {'caption': 'Subclim: java_refactor_rename',
  'command': 'subclim_java_refactoring_rename'},
 {'caption': 'Subclim: java_refactor_redo',
  'command': 'subclim_java_refactoring_redo'},
 {'caption': 'Subclim: java_correct', 'command': 'subclim_java_code_correct'},
 {'caption': 'Subclim: java_classpath_variables',
  'command': 'subclim_java_classpath_variables'},
 {'caption': 'Subclim: webxml_validate',
  'command': 'subclim_java_webxml_validate'},
 {'caption': 'Subclim: java_delegate', 'command': 'subclim_java_delegate'},
 {'caption': 'Subclim: java_import_missing',
  'command': 'subclim_java_include_import_missing'},
 {'caption': 'Subclim: javadoc_comment',
  'command': 'subclim_java_doc_comment'},
 {'caption': 'Subclim: java_complete',
  'command': 'subclim_java_code_complete'},
 {'caption': 'Subclim: java_src_update', 'command': 'subclim_java_src_update'},
 {'caption': 'Subclim: java_checkstyle', 'command': 'subclim_java_checkstyle'},
 {'caption': 'Subclim: java_imports_unused',
  'command': 'subclim_java_include_unused_imports'},
 {'caption': 'Subclim: java_classpath', 'command': 'subclim_java_classpath'},
 {'caption': 'Subclim: java_format', 'command': 'subclim_java_format'},
 {'caption': 'Subclim: java_classpath_variable_create',
  'command': 'subclim_java_classpath_variable_create'},
 {'caption': 'Subclim: java_junit_impl',
  'command': 'subclim_java_junit_j_unit_impl'},
 {'caption': 'Subclim: ant_targets', 'command': 'subclim_ant_run_targets'},
 {'caption': 'Subclim: java_src_exists',
  'command': 'subclim_java_src_file_exists'},
 {'caption': 'Subclim: ant_complete', 'command': 'subclim_ant_code_complete'},
 {'caption': 'Subclim: java', 'command': 'subclim_java_src_run'},
 {'caption': 'Subclim: maven_dependency_search',
  'command': 'subclim_maven_dependency_search'},
 {'caption': 'Subclim: ant_validate', 'command': 'subclim_ant_validate'},
 {'caption': 'Subclim: java_search', 'command': 'subclim_java_search'},
 {'caption': 'Subclim: reload', 'command': 'subclim_eclipse_reload'},
 {'caption': 'Subclim: archive_read', 'command': 'subclim_core_archive_read'},
 {'caption': 'Subclim: jobs', 'command': 'subclim_core_eclipse_jobs'},
 {'caption': 'Subclim: project_build',
  'command': 'subclim_core_project_build'},
 {'caption': 'Subclim: locate_file',
  'command': 'subclim_core_search_locate_file'},
 {'caption': 'Subclim: settings_update',
  'command': 'subclim_core_settings_update'},
 {'caption': 'Subclim: project_delete',
  'command': 'subclim_core_project_delete'},
 {'caption': 'Subclim: settings', 'command': 'subclim_core_settings'},
 {'caption': 'Subclim: project_move', 'command': 'subclim_core_project_move'},
 {'caption': 'Subclim: xml_validate', 'command': 'subclim_core_xml_validate'},
 {'caption': 'Subclim: workspace_dir',
  'command': 'subclim_core_eclipse_workspace'},
 {'caption': 'Subclim: history_revision',
  'command': 'subclim_core_history_revision'},
 {'caption': 'Subclim: project_nature_aliases',
  'command': 'subclim_core_project_nature_aliases'},
 {'caption': 'Subclim: project_update',
  'command': 'subclim_core_project_update'},
 {'caption': 'Subclim: project_open', 'command': 'subclim_core_project_open'},
 {'caption': 'Subclim: project_create',
  'command': 'subclim_core_project_create'},
 {'caption': 'Subclim: project_refresh',
  'command': 'subclim_core_project_refresh'},
 {'caption': 'Subclim: ping', 'command': 'subclim_core_ping'},
 {'caption': 'Subclim: project_setting',
  'command': 'subclim_core_project_setting'},
 {'caption': 'Subclim: shutdown', 'command': 'subclim_core_shutdown'},
 {'caption': 'Subclim: history_clear',
  'command': 'subclim_core_history_clear'},
 {'caption': 'Subclim: xml_format', 'command': 'subclim_core_xml_format'},
 {'caption': 'Subclim: problems', 'command': 'subclim_core_problems'},
 {'caption': 'Subclim: project_settings',
  'command': 'subclim_core_project_settings'},
 {'caption': 'Subclim: project_nature_add',
  'command': 'subclim_core_project_nature_add'},
 {'caption': 'Subclim: project_by_resource',
  'command': 'subclim_core_project_by_resource'},
 {'caption': 'Subclim: project_link_resource',
  'command': 'subclim_core_project_link_resource'},
 {'caption': 'Subclim: history_list', 'command': 'subclim_core_history_list'},
 {'caption': 'Subclim: project_close',
  'command': 'subclim_core_project_close'},
 {'caption': 'Subclim: history_add', 'command': 'subclim_core_history_add'},
 {'caption': 'Subclim: projects', 'command': 'subclim_core_projects'},
 {'caption': 'Subclim: project_info', 'command': 'subclim_core_project_info'},
 {'caption': 'Subclim: project_list', 'command': 'subclim_core_project_list'},
 {'caption': 'Subclim: project_natures',
  'command': 'subclim_core_project_natures'},
 {'caption': 'Subclim: project_refresh_file',
  'command': 'subclim_core_project_refresh_file'},
 {'caption': 'Subclim: project_import',
  'command': 'subclim_core_project_import'},
 {'caption': 'Subclim: project_nature_remove',
  'command': 'subclim_core_project_nature_remove'},
 {'caption': 'Subclim: project_rename',
  'command': 'subclim_core_project_rename'},
 {'caption': 'Subclim: dltk_buildpaths',
  'command': 'subclim_dynamic_buildpaths'},
 {'caption': 'Subclim: dltk_buildpath_variable_create',
  'command': 'subclim_dynamic_buildpath_variable_create'},
 {'caption': 'Subclim: dltk_interpreters',
  'command': 'subclim_dynamic_launching_interpreters'},
 {'caption': 'Subclim: dltk_remove_interpreter',
  'command': 'subclim_dynamic_launching_delete_interpreter'},
 {'caption': 'Subclim: dltk_buildpath_variable_delete',
  'command': 'subclim_dynamic_buildpath_variable_delete'},
 {'caption': 'Subclim: dltk_search', 'command': 'subclim_dynamic_search'},
 {'caption': 'Subclim: dltk_add_interpreter',
  'command': 'subclim_dynamic_launching_add_interpreter'},
 {'caption': 'Subclim: dltk_buildpath_variables',
  'command': 'subclim_dynamic_buildpath_variables'},
 {'caption': 'Subclim: php_src_update', 'command': 'subclim_php_src_update'},
 {'caption': 'Subclim: php_complete', 'command': 'subclim_php_code_complete'},
 {'caption': 'Subclim: php_search', 'command': 'subclim_php_search'},
 {'caption': 'Subclim: c_src_update', 'command': 'subclim_clang_src_update'},
 {'caption': 'Subclim: c_project_src',
  'command': 'subclim_clang_project_source_entry'},
 {'caption': 'Subclim: c_sourcepaths',
  'command': 'subclim_clang_project_source_paths'},
 {'caption': 'Subclim: c_includepaths',
  'command': 'subclim_clang_project_include_paths'},
 {'caption': 'Subclim: c_search', 'command': 'subclim_clang_search'},
 {'caption': 'Subclim: c_project_configs',
  'command': 'subclim_clang_project_configurations'},
 {'caption': 'Subclim: c_project_symbol',
  'command': 'subclim_clang_project_symbol_entry'},
 {'caption': 'Subclim: c_project_include',
  'command': 'subclim_clang_project_include_entry'},
 {'caption': 'Subclim: c_callhierarchy',
  'command': 'subclim_clang_call_hierarchy'},
 {'caption': 'Subclim: c_complete', 'command': 'subclim_clang_code_complete'},
 {'caption': 'Subclim: xsd_validate', 'command': 'subclim_web_xsd_validate'},
 {'caption': 'Subclim: html_complete',
  'command': 'subclim_web_html_code_complete'},
 {'caption': 'Subclim: html_validate', 'command': 'subclim_web_html_validate'},
 {'caption': 'Subclim: javascript_complete',
  'command': 'subclim_web_java_script_code_complete'},
 {'caption': 'Subclim: css_validate', 'command': 'subclim_web_css_validate'},
 {'caption': 'Subclim: javascript_src_update',
  'command': 'subclim_web_java_script_src_update'},
 {'caption': 'Subclim: css_complete',
  'command': 'subclim_web_css_code_complete'},
 {'caption': 'Subclim: xml_complete',
  'command': 'subclim_web_xml_code_complete'},
 {'caption': 'Subclim: dtd_validate', 'command': 'subclim_web_dtd_validate'},
 {'caption': 'Subclim: ruby_src_update', 'command': 'subclim_ruby_src_update'},
 {'caption': 'Subclim: ruby_complete',
  'command': 'subclim_ruby_code_complete'},
 {'caption': 'Subclim: ruby_search', 'command': 'subclim_ruby_search'},
 {'caption': 'Subclim: ruby_add_interpreter',
  'command': 'subclim_ruby_launching_add_interpreter'}]
'''