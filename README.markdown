Subclim
-------

This plugin integrates Sublime Text 2 with Eclipse via Eclim http://eclim.org/.
At the moment it adds Java completions, auto-import, goto-definition, goto-usages and compilation/validation (error highlighting).

**New**: It is possible to get Scala validation and completions, but you will need to install the scala-ide branch of Eclim manually (clone their repo, checkout scala-ide and build with Ant as described there).

**Also New**: Subclim will not automatically provide completions by default, but only on
manual request (ctrl+alt+space). There is an option "subclim_auto_complete" to turn the old behaviour back on. As the Eclim completions are quite slow, I find it much more efficient to use ST2 native buffer-based completion 90% of the time, and manually trigger the Eclim-completions when I really need them. Your mileage may vary.

Installation
-----------

Just add the plugin to your Sublime Text packages directory as usual.
Additionally, install Eclim from eclim.org. Then, in Sublime Text run the command set_eclim_path
via the command palette to tell ST2 where to find eclim.

**Important**: This plugin is only compatible with Eclim version 1.7.3 or greater.

Usage
-----

Either run Eclipse and open the Eclim View, or run eclimd from a console.
I recommend the first way, as you still need Eclipse for project management tasks. While you are coding, you can just keep Eclipse minimized, as long as the Eclim View has been opened.

The plugin will only work when editing files inside an open Eclipse project. Compilation/validation will be done asynchronously on load and save, to keep editing fluent, so errors may not appear instantly, but after a few seconds.
The very first command or completion on startup can take very long. Subsequent ones will be quicker. Completions are not automatically triggered with ST2 normal completions, but manually with ctrl+alt+space. You can change this behaviour in the settings ("subclim_auto_complete").

To see the available commands and their keybindings, just use the command pallete and
enter "Subclim".

Most other Eclim commands might be available too, but are not supported. Check generated.py and set keybindings for the commands there if you are feeling adventurous.
