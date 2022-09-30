# Changelog

## v0.8.0 - 2022-09-30

The release started as a minor one to add support for includes (#4). But ended up as quite a big one, because recent releases of Taskfile added features, which allowed removal of `pyyaml` dependency and bumping internal python version to `3.8`.

Here goes a proper list of changes:

- add support for includes by utilizing `--list-all` flag (#4)
- remove `pyyaml` dependency
- bump internal python version to `3.8`
- bump dev dependencies
- update README regarding python version, features and installation

## v0.7.0 - 2021-07-16

Refactor and improve multiple folders handling.

## v0.6.0 - 2021-07-08

Taskfile initialization improvements

- Fix Taskfile initialization
- Open Taskfile after initialization with a small delay
- Properly handle Taskfile initialization if multiple folders are opened

## v0.5.1 - 2021-07-06

Update readme regarding python version.

## v0.5.0 - 2021-07-05

I had to rewrite the plugin to support Python 3.3, because there are some issues (https://github.com/wbond/package_control/issues/1570#issue-900010126) with loading Python 3.8 modules.

The previous work lives at `python38` branch and will be braught back once the issue is resolved.

## v0.4.1 - 2021-07-05

- Remove `.python-version` from export-ignore

## v0.4.0 - 2021-07-05

- Add `Taskfile: Init` command

## v0.3.4 - 2021-07-04

- Remove `.python-version` from my global `.gitignore` to fix the issue when plugin picked up wrong python version (3.3 instead of 3.8)

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
