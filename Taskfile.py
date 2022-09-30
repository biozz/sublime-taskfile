import os
import subprocess
import time
from functools import partial

import sublime
import sublime_plugin

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
        items = self.get_tasks_quick_panel_items(folder)
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

    def get_tasks_quick_panel_items(self, folder):
        result = []
        # -s flag (silent output) will not work here, because I need task descriptions
        # the downside is that I have to parse human-readable output of the command
        list_all_result = subprocess.run(
            ["task", "--list-all"], capture_output=True, cwd=folder
        )
        if list_all_result.returncode != 0:
            print(list_all_result.stderr.decode())
            self.window.status_message(
                "Unable list tasks: see Sublime's console for more info"
            )
            return []
        # Stdout is sliced because the first line is a general Taskfile message
        tasks = list_all_result.stdout.decode().split("* ")[1:]
        for task in tasks:
            name_raw, summary_raw = task.split("\t")
            # The name of each task ends with colon and a space, they need to be removed
            name = name_raw[:-2]
            summary = summary_raw.strip().replace("\n\n", "\n").split("\n")
            item = sublime.QuickPanelItem(name, summary)
            result.append(item)
        return result

    def get_folders_quick_panel_items(self, folders):
        return [sublime.QuickPanelItem(os.path.basename(f)) for f in folders]


def get_folders_with_taskfile(folders):
    return list(
        filter(lambda x: os.path.exists(os.path.join(x, TASKFILE_NAME)), folders)
    )
