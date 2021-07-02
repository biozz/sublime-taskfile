# Changelog

## v0.3.3 - 2021-07-02

- Update `README.md` with notes about installation and linting of the source code

## v0.3.2 - 2021-07-01

- Fix `messages.json` format

## v0.3.1 - 2021-06-29

- Add `.gitattributes` with `export-ignore` directives

## v0.3.0 - 2021-06-29

- Remove vendor and use Package Control's `pyyaml` dependency

## v0.2.0 - 2021-05-30

- Add handling of project folders
- Fix working directory of the Taskfile
- Remove unused `os` import
- Refactor paths to use `pathlib.Path`
- Fix handling of exit from `Run Task` menu via `Esc`

## v0.1.1 - 2021-05-29

Fix versions in messages.

## v0.1.0 - 2021-05-29

- Add `poetry`
- Add license
- Add changelog
- Reformat with `black`, `isort` and `autoflake`
- Add more PyYAML versions for different architectures
- Add task summary
- Use [QuickPanelItem](https://www.sublimetext.com/docs/api_reference.html#sublime.QuickPanelItem) instead of plain text keys
- Add usage gif

## v0.0.3 - 2021-05-27

- Fix indent

## v0.0.2 - 2021-05-27

- Move `Taskfile.yml` loading into `run`

## v0.0.1 - 2021-05-27

Initial version
