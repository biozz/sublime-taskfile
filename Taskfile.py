import os
import time
from functools import partial

import sublime
import sublime_plugin
import yaml

TASKFILE_NAME = "Taskfile.yml"


class InitCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self.window.folders()
        if not folders:
            self.window.status_message("You have to be in a directory for init to work")
            return
        folders_with_taskfile = get_folders_with_taskfile(folders)
        folders_without_taskfile = list(set(folders) - set(folders_with_taskfile))
        if len(folders_without_taskfile) == 0:
            self.window.status_message("Taskfile exists in all open folders")
            return
        if len(folders_without_taskfile) == 1:
            self.initialize_taskfile(folders_without_taskfile, 0)
            return
        on_done = partial(self.initialize_taskfile, folders)
        self.window.show_quick_panel(folders, on_done)

    def initialize_taskfile(self, quick_panel_items, index):
        if index < 0:
            return
        self.window.run_command(
            "exec",
            args={"shell_cmd": "task -i", "working_dir": quick_panel_items[index]},
        )
        # It is nice to have initialized file opened in the editor after creation.
        # The problem is Sublime Text is too fast and opens empty file, so I added
        # a small timeout for openning.
        taskfile_path = os.path.join(quick_panel_items[index], TASKFILE_NAME)
        open_file = partial(self.window.open_file, taskfile_path)
        sublime.set_timeout(open_file, 500)


class RunTaskCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders_with_taskfile = get_folders_with_taskfile(self.window.folders())
        if not folders_with_taskfile:
            self.window.status_message("You have to be in a directory with Taskfile")
            return
        if len(folders_with_taskfile) > 1:
            self.select_folder(folders_with_taskfile)
            return
        self.select_task(folders_with_taskfile, 0)

    def select_folder(self, folders):
        on_done = partial(self.select_task, folders)
        items = self.get_folders_quick_panel_items(folders)
        self.window.show_quick_panel(items, on_done)

    def select_task(self, folders, index):
        if index < 0:
            return
        folder = folders[index]
        taskfile_path = os.path.join(folder, TASKFILE_NAME)
        res = yaml.load(open(taskfile_path), Loader=yaml.FullLoader)
        items = self.get_tasks_quick_panel_items(res)
        on_done = partial(self.run_task, items, str(folder))
        self.window.show_quick_panel(items, on_done)

    def run_task(self, quick_panel_items, working_dir, index):
        if index < 0:
            return
        task_name = quick_panel_items[index].trigger
        self.window.run_command(
            "exec",
            args={
                "shell_cmd": "task {task_name}".format(task_name=task_name),
                "working_dir": working_dir,
            },
        )

    def get_tasks_quick_panel_items(self, taskfile):
        result = []
        for task_name, task in taskfile.get("tasks").items():
            summary = task.get("summary")
            if summary:
                summary = summary.split("\n")[0]
            item = sublime.QuickPanelItem(task_name, summary)
            result.append(item)
        return result

    def get_folders_quick_panel_items(self, folders):
        return [sublime.QuickPanelItem(os.path.basename(f)) for f in folders]


def get_folders_with_taskfile(folders):
    return list(
        filter(lambda x: os.path.exists(os.path.join(x, TASKFILE_NAME)), folders)
    )
