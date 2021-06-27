# Sublime Taskfile

A Sublime Text 4 plugin for running tasks from [Taskfile](https://taskfile.dev). It adds `Taskfile: Run Task` to your command palette and you can select which task to run. The output of the task is than displayed in the quick panel on the bottom.

![Usage](Usage.gif)

## Caveats

- made for Sublime Text 4
- uses [Sublime's python version 3.8](https://www.sublimetext.com/docs/api_environments.html#selecting_python_version)
- has a vendored package - PyYAML 5.4.1 (tested only with MacOS X)

## Installation

The plugin is still waiting for approval at package control repo ([!8283](https://github.com/wbond/package_control_channel/pull/8283)), so it is not possible install via Package Control at the moment.

## Contributing

You are welcome to submit pull requests with bug fixes and improvements.

Please lint your files with `task lint` before submition.
