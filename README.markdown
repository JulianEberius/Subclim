Subclim
-------

This plugin integrates Sublime Text 2 with Eclipse via Eclim http://eclim.org/.
At the moment it adds Java completions, auto-import, goto-definition and compilation/validation (error highlighting).

Installation
-----------

Just add the plugin to your Sublime Text packages directory as usual.
Additionally, install Eclim from eclim.org. Then, in Sublime Text run the command set_eclim_path
via the command palette to tell ST2 where to find eclim.
*Important*: This plugin is only compatible with Eclim version 1.7.3 or greater.
*Important 2*: I would recommend to disable ST2's "as-you-type" completion when working with Subclim (setting "auto_complete" to false). For bigger projects, the Eclim completions can not keep up and might mess up your typing. Just find out whether it works for you.

Usage
-----

Either run Eclipse and open the Eclim View, or run eclimd from a console.
I recommend the first way,as you still need Eclipse for project management tasks. While you are coding, you can just keep Eclipse minimized, as long as the Eclim View has been opened.

The plugin will only work when editing files inside an open Eclipse project.
The very first command or completion on startup can take very long. Subsequent ones will be quicker.

For keybindings see the keymaps in the plugin's directory (or the command palette).
In addition to completions, the following commands are supported at the moment:

- Go to definition
- Import class under cursor
- Run current class as Java application

Most other Eclim commands might be available too, but are not supported. Check generated.py and set keybindings for the commands there if you are feeling adventurous.
