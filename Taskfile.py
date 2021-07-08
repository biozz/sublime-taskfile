import os
from functools import partial

import sublime
import sublime_plugin
import yaml
import time


TASKFILE_NAME = "Taskfile.yml"


class InitCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self.window.folders()
        if not folders:
            self.window.status_message("You have to be in a directory for init to work")
            return
        folders = list(
            filter(
                lambda x: not os.path.exists(os.path.join(x, TASKFILE_NAME)), folders
            )
        )
        if not folders:
            self.window.status_message("Taskfile exists in all open folders.")
        if len(folders) == 1:
            initialize_taskfile(self.window, folders, 0)
            return
        on_done = partial(initialize_taskfile, self.window, folders)
        self.window.show_quick_panel(folders, on_done)


class RunTaskCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self.window.folders()
        if not folders or len(folders) > 1:
            self.window.status_message("Only one folder per project is supported.")
            return
        working_dir_path = folders[0]
        taskfile_path = os.path.join(working_dir_path, "Taskfile.yml")
        res = yaml.load(open(taskfile_path), Loader=yaml.FullLoader)
        items = get_quick_panel_items(res)
        on_done = partial(run_task_by_index, self.window, items, str(working_dir_path))
        self.window.show_quick_panel(items, on_done, sublime.MONOSPACE_FONT)


def initialize_taskfile(window, quick_panel_items, index):
    if index < 0:
        return
    window.run_command(
        "exec", args={"shell_cmd": "task -i", "working_dir": quick_panel_items[index]}
    )
    # It is nice to have initialized file opened in the editor after creation.
    # The problem is Sublime Text is too fast and opens empty file, so I added
    # a small timeout for openning.
    taskfile_path = os.path.join(quick_panel_items[index], TASKFILE_NAME)
    open_file = partial(window.open_file, taskfile_path)
    sublime.set_timeout(open_file, 500)


def run_task_by_index(window, quick_panel_items, working_dir, index):
    if index < 0:
        return
    task_name = quick_panel_items[index].trigger
    window.run_command(
        "exec",
        args={
            "shell_cmd": "task {task_name}".format(task_name=task_name),
            "working_dir": working_dir,
        },
    )


def get_quick_panel_items(taskfile):
    result = []
    for task_name, task in taskfile.get("tasks").items():
        summary = task.get("summary")
        if summary:
            summary = summary.split("\n")[0]
        item = sublime.QuickPanelItem(task_name, summary)
        result.append(item)
    return result
