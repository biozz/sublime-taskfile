import importlib.util
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


class QuickPanelItem:
    def __init__(self, trigger, details=None):
        self.trigger = trigger
        self.details = details


# Sublime provides these modules inside its plugin host only.
sys.modules["sublime"] = types.SimpleNamespace(
    QuickPanelItem=QuickPanelItem, set_timeout=Mock()
)
sys.modules["sublime_plugin"] = types.SimpleNamespace(WindowCommand=object)
spec = importlib.util.spec_from_file_location(
    "taskfile_plugin", Path(__file__).resolve().parents[1] / "Taskfile.py"
)
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)


class TaskfileTests(unittest.TestCase):
    def setUp(self):
        self.command = plugin.RunTaskCommand()
        self.command.window = Mock()

    def test_parse_tabs_spaces_namespaces_and_multiline_descriptions(self):
        output = (
            "task: Available tasks for this project:\n"
            "* build:       Build with * special text\n"
            "* app:test:\tRun tests\n  More details\n"
            "* empty:       \n"
        )
        with patch.object(plugin.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, output, "")
            items = self.command.get_tasks_quick_panel_items("/project")
        self.assertEqual(
            [item.trigger for item in items], ["build", "app:test", "empty"]
        )
        self.assertEqual(items[0].details, ["Build with * special text"])
        self.assertEqual(items[1].details, ["Run tests", "  More details"])

    def test_failed_task_listing(self):
        with patch.object(plugin.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 1, "", "bad taskfile")
            self.assertEqual(self.command.get_tasks_quick_panel_items("/project"), [])
        self.command.window.status_message.assert_called_once()

    def test_missing_executable_and_timeout(self):
        for error in (FileNotFoundError("task"), subprocess.TimeoutExpired("task", 30)):
            with self.subTest(error=error), patch.object(
                plugin.subprocess, "run", side_effect=error
            ):
                self.assertEqual(
                    self.command.get_tasks_quick_panel_items("/project"), []
                )

    def test_execution_preserves_task_as_single_argument(self):
        self.command.run_task([QuickPanelItem("build; echo surprise")], "/project", 0)
        self.command.window.run_command.assert_called_once_with(
            "exec",
            args={"cmd": ["task", "build; echo surprise"], "working_dir": "/project"},
        )

    def test_cancel_does_not_execute(self):
        self.command.run_task([], "/project", -1)
        self.command.select_task([], -1)
        self.command.window.run_command.assert_not_called()

    def test_empty_listing_does_not_open_panel(self):
        with patch.object(self.command, "get_tasks_quick_panel_items", return_value=[]):
            self.command.select_task(["/project"], 0)
        self.command.window.show_quick_panel.assert_not_called()

    def test_recognized_taskfile_names(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in (
                "Taskfile.yml",
                "Taskfile.yaml",
                "taskfile.yml",
                "taskfile.yaml",
                "Taskfile.dist.yml",
                "Taskfile.dist.yaml",
                "taskfile.dist.yml",
                "taskfile.dist.yaml",
            ):
                with self.subTest(name=name):
                    path = Path(folder, name)
                    path.touch()
                    self.assertEqual(
                        plugin.get_folders_with_taskfile([folder]), [folder]
                    )
                    path.unlink()
            os.mkdir(os.path.join(folder, "Taskfile.yml"))
            self.assertEqual(plugin.get_folders_with_taskfile([folder]), [])

    def test_init_only_offers_folders_without_taskfiles_in_project_order(self):
        command = plugin.InitCommand()
        command.window = Mock()
        command.window.folders.return_value = ["/a", "/b", "/c"]
        with patch.object(plugin, "get_folders_with_taskfile", return_value=["/b"]):
            command.run()
        items, callback = command.window.show_quick_panel.call_args[0]
        self.assertEqual(items, ["/a", "/c"])
        callback(1)
        command.window.run_command.assert_called_once_with(
            "exec", args={"cmd": ["task", "--init"], "working_dir": "/c"}
        )


if __name__ == "__main__":
    unittest.main()
