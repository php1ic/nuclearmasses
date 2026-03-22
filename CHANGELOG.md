# Changelog

## [0.0.5] - 2026-03-22
- Fix bug that was creating a new column to update a single value, rather than updating value in existing column [a420c33](https://github.com/php1ic/nuclearmasses/commit/a420c332d1ff76ed32156c2f4d6e86c9e4e2375f)
- Refactor NUBASE parsing [#15](https://github.com/php1ic/nuclearmasses/issues/15)
- Remove use of try/catch block when parsing the files [#16](https://github.com/php1ic/nuclearmasses/issues/16)

## [0.0.4] - BREAKING CHANGES - 2026-03-14
- BREAKING: Change project structure to aid scalability and maintainability [#10](https://github.com/php1ic/nuclearmasses/issues/10)
  * Accessing the top level mass table has not changed, but the user **must** import via a submodule, e.g. `io` or `utils` to use the underlying functions.

## [0.0.3] - 2026-02-21
- Change file parsing to make use of the read_fwf() in pandas [#2](https://github.com/php1ic/nuclearmasses/pull/2)
- Add various static code checker configs (isort, ruff, mypy) and make necessary changes [#8](https://github.com/php1ic/nuclearmasses/pull/8)
- Create new columns that contain half-life values, and their error, in seconds [#9](https://github.com/php1ic/nuclearmasses/pull/9)
- Update parsing to fix bug related to pandas [v3 migration](https://pandas.pydata.org/docs/dev/user_guide/migration.html#brief-introduction-to-the-new-default-string-dtype) [62cc9d08](https://github.com/php1ic/nuclearmasses/commit/62cc9d08427052fb9cc841369f11f71de16743ac)
- Automate deployment to pypi when a new version (tag) is created [#3](https://github.com/php1ic/nuclearmasses/issues/3)

## [0.0.2] - 2026-02-21
- Version bump to test auto deployment to pypi. Included here so future readers don't wonder why it was skipped

## [0.0.1] - 2025-03-25
- Initial version and release
