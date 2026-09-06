# Contributing

Contributions to `nuclearmasses` are welcome!


## Reporting issues

If you have ideas for additional functionality or find bugs please create an [issue](https://github.com/php1ic/nuclearmasses/issues).
If you're unsure whether an idea fits the project, feel free to open an issue anyway to discuss it.


## Development setup

Clone the repository and install the package in an editable environment with the development dependencies:
```bash
git clone https://github.com/php1ic/nuclearmasses
cd nuclearmasses
# Create a suitable environment if required
pip install -e '.[dev]'
```

## Running the tests

The module use [pytest](https://docs.pytest.org/en/stable/) which is run with
```bash
pytest -v
```
Please add tests as appropriate when making changes to the code.


## Static analysis and linting

We use a combination of [ruff](https://docs.astral.sh/ruff/) and [mypy](https://www.mypy-lang.org/) to keep things tidy and hopefully catch errors and bugs before they happen.
The command below returns no errors or issues so should be run after any code changes.
We might add a dedicated linting and static analysis CI pipeline in the future, but for the moment, it's a manual process.
```bash
ruff format && ruff check && mypy src
```
Checking is also done with [ty](https://github.com/astral-sh/ty), but as that is [not yet stable](https://github.com/astral-sh/ty#version-policy), any issues it flags are not yet considered issues.
Having said that, all checks currently pass with
```bash
ty check
```
## Documentation

Clone the repository and install the package in an editable environment with the documentation dependencies:
```bash
git clone https://github.com/php1ic/nuclearmasses
cd nuclearmasses
# Create a suitable environment if required
pip install -e '.[docs]'
```

The documentation can be built with:
```bash
sphinx-build -W -b html docs/source docs/build
```
Or, to spawn a server that allows you to see edits in real time, an additional module can be installed.
```bash
pip install sphinx auto-build
sphinx-autobuild docs/source docs/build
```
The `sphinx-autobuild` package is more quality of life for iterating document edits than required for functionality.
For this reason, it has not been added to the `pyproject.toml` file to be automatically installed.


## Pull requests

Please open a [pull request](https://github.com/php1ic/nuclearmasses/pulls) against the `main` branch.
New functionality should include appropriate passing tests, not introduce any new static analysis or linting warnings, and documentation where applicable.
Please don't worry about having everything complete before opening a pull request. The idea is the most important part.
If tests, linting, static analysis, or documentation are still needed, open the PR anyway and we can work together to get it ready for merging.
