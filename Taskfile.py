import os
import zipimport

from pathlib import Path
from functools import partial

import sublime_plugin


cwd = Path(__file__).parent
pack_path = cwd / 'vendor/PyYAML-5.4.1-cp38-cp38-macosx_10_9_x86_64.whl'
importer = zipimport.zipimporter(pack_path.resolve())
yaml = importer.load_module('yaml')


class RunTaskCommand(sublime_plugin.WindowCommand):
	def run(self):
        taskfile = open(cwd / 'Taskfile.yml')
        res = yaml.load(taskfile, Loader=yaml.FullLoader)
        tasks_keys = list([t for t in res.get('tasks')])
		on_done = partial(run_task_by_index, self.window)
		self.window.show_quick_panel(tasks_keys, on_done)

def run_task_by_index(window, task_index):
	window.run_command('exec', args={'shell_cmd': f'task {tasks_keys[task_index]}'})
