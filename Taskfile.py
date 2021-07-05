import os
from functools import partial

import sublime
import sublime_plugin
import yaml


class InitCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self.window.folders()
        if not folders:
            self.window.status_message("You have to be in a directory for init to work")
            return
        # TODO: check if Taskfile has been initialized already and filter out these folders
        if len(folders) > 1:
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
    window.run_command(
        "exec", args={"shell_cmd": "task -i", "working_dir": quick_panel_items[index]}
    )


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
