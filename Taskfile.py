import os
import zipimport
from functools import partial
from pathlib import Path

import sublime
import sublime_plugin

cwd = Path(__file__).parent


PLATFORM_TO_ARCH_TO_WHL = {
    "osx": {
        "x64": "PyYAML-5.4.1-cp38-cp38-macosx_10_9_x86_64.whl",
    },
    "linux": {
        "x64": "PyYAML-5.4.1-cp38-cp38-manylinux1_x86_64.whl",
        "arm64": "PyYAML-5.4.1-cp38-cp38-manylinux2014_aarch64.whl",
    },
    "windows": {
        "x86": "PyYAML-5.4.1-cp38-cp38-win32.whl",
        "x64": "PyYAML-5.4.1-cp38-cp38-win_amd64.whl",
    },
}
platform = sublime.platform()
arch = sublime.arch()
whl = PLATFORM_TO_ARCH_TO_WHL.get(platform, {}).get(arch)
if not whl:
    raise Exception("This platform or architecture is not supported")
pack_path = cwd / "vendor" / whl
importer = zipimport.zipimporter(pack_path.resolve())
yaml = importer.load_module("yaml")


class RunTaskCommand(sublime_plugin.WindowCommand):
    def run(self):
        taskfile = open(cwd / "Taskfile.yml")
        res = yaml.load(taskfile, Loader=yaml.FullLoader)
        items = get_quick_panel_items(res)
        on_done = partial(run_task_by_index, self.window, items)
        self.window.show_quick_panel(items, on_done, sublime.MONOSPACE_FONT)


def run_task_by_index(window, quick_panel_items, index):
    task_name = quick_panel_items[index].trigger
    window.run_command("exec", args={"shell_cmd": f"task {task_name}"})


def get_quick_panel_items(taskfile):
    result = []
    for task_name, task in taskfile.get("tasks").items():
        summary = task.get("summary")
        if summary:
            summary = summary.split("\n")[0]
        item = sublime.QuickPanelItem(task_name, summary)
        result.append(item)
    return result
