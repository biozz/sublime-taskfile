# Sublime Taskfile

![Package Control](https://img.shields.io/packagecontrol/dt/Taskfile)

A Sublime Text 4 plugin for running tasks from [Taskfile](https://taskfile.dev). It adds `Taskfile: Run Task` to your command palette and you can select which task to run. The output of the task is then displayed in the quick panel on the bottom.

It is also possible to initialize the `Taskfile` with `Taskfile: Init` command, which basically does `task -i` in one of the project directories you choose.

![Usage](Usage.gif)

- made for Sublime Text 4
- has no external dependencies (other than `task` command)
- properly handles multiple open directories
- supports taskfile includes
- does not and will not ship any custom syntax definitions (see installation notes for more details)

## Installation

First, [install Taskfile command](https://taskfile.dev/installation/).

Then use `Package Control: Install Package` command and search for `Taskfile`.

If you want to have a hints on which keys are available and what they do, there is an [official JSON schema for Taskfile](https://json.schemastore.org/taskfile.json), which can be loaded automatically once you install [LSP](packagecontrol.io/packages/LSP) and [LSP-yaml](https://packagecontrol.io/packages/LSP-yaml) packages.

## Contributing

You are welcome to submit pull requests with bug fixes and improvements.

Please lint your files with `black` before submition.
