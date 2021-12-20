# game

### Install

1. Clone repo

```bash
git clone https://github.com/a1d4r/last-letter-game.git
cd last-letter-game
```

2. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

3. Initialize poetry and python package:

```bash
make install
```

### Usage

```
Usage: last-letter [OPTIONS]             

Options:
  --host TEXT                     [default: 127.0.0.1]
  --port INTEGER                  [default: 1234]
  --name TEXT
  --redis-dsn TEXT                [default: redis://127.0.0.1:6379/0]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```


### Makefile usage

[`Makefile`](https://github.com/a1d4r/game/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort`, `autoflake` and `black`.

```bash
make codestyle

# or use synonym
make format
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black`, `autoflake` and `darglint` library

</p>
</details>

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-security
```

This command identifies security issues with `Safety` and `Bandit`.

```bash
make check-security
```

To validate `pyproject.toml` use
```bash
make check-poetry
```


</p>
</details>

<details>
<summary>5. Linting and type checks</summary>
<p>

Run static linting with `pylint` and `mypy`:

```bash
make static-lint
```

</p>
</details>

<details>
<summary>6. Tests</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make static-lint && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/a1d4r/game/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Or to remove pycache, build and docker image run:

```bash
make clean-all
```

</p>
</details>
