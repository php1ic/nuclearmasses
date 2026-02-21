# Changelog

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
