from functools import partial
from pathlib import Path

import sublime
import sublime_plugin
import yaml


class RunTaskCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self.window.folders()
        if not folders or len(folders) > 1:
            self.window.status_message("Only one folder per project is supported.")
            return
        working_dir_path = Path(folders[0])
        taskfile_path = working_dir_path / "Taskfile.yml"
        res = yaml.load(taskfile_path.open(), Loader=yaml.FullLoader)
        items = get_quick_panel_items(res)
        on_done = partial(run_task_by_index, self.window, items, str(working_dir_path))
        self.window.show_quick_panel(items, on_done, sublime.MONOSPACE_FONT)


def run_task_by_index(window, quick_panel_items, working_dir, index):
    if index < 0:
        return
    task_name = quick_panel_items[index].trigger
    window.run_command(
        "exec", args={"shell_cmd": f"task {task_name}", "working_dir": working_dir}
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
