# pymqi-embedded

`pymqi-embedded` is a fork of the [PyMQI](https://pypi.org/project/pymqi/) bindings for the IBM MQ
messaging system. The project packages the IBM MQ Client runtime inside the wheel so
that users do not need a system wide installation of the MQ libraries.

## Features

- Works with Python 3.8 through 3.12.
- Linux wheels are built as `manylinux2014_x86_64` (or `manylinux_2_28_x86_64`).
- Windows wheels bundle the required DLLs using [delvewheel](https://github.com/adang1345/delvewheel).
- Pure Python API compatible with `pymqi` while keeping the import name `pymqi`.

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency
management and `setuptools` for building the C extension. After cloning the
repository run:

```bash
poetry install
```

### Running the linters and tests

```bash
poetry run ruff src tests
poetry run black --check src tests
poetry run mypy src
poetry run pytest
```

## Building wheels

### Linux

The `scripts/build_manylinux.sh` helper is intended to run inside a
`manylinux2014` or `manylinux_2_28` container. It installs the IBM MQ runtime,
loops over the supported Python versions and produces repaired wheels using
`auditwheel`.

### Windows

Use the PowerShell script `scripts/build_windows.ps1` in a Visual Studio
Developer Command Prompt. The script builds the extension for the supported
Python versions and repairs the wheels with `delvewheel`.

### Smoke test

The `scripts/smoke_test.py` script performs a simple put/get round trip. It
requires the `MQSERVER` environment variable to be set pointing at a running MQ
queue manager.

## License

The Python sources are distributed under a proprietary license. The IBM MQ
Client is redistributed under the IBM license terms. Consult `LICENSE` for
details.
