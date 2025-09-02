# pymqi-embedded

`pymqi-embedded` embeds the [PyMQI](https://github.com/pymqi/pymqi) bindings for the IBM MQ
messaging system and bundles the IBM MQ Client runtime inside the wheel so that users do not
need a system wide installation of the MQ libraries. The project is safe to run under
`python -m compileall` because all native components are loaded lazily.

## Features

- Works with Python 3.8 through 3.12.
- Linux wheels are built as `manylinux2014_x86_64` (or `manylinux_2_28_x86_64`).
- Windows wheels bundle the required DLLs using [delvewheel](https://github.com/adang1345/delvewheel).
- Pure Python API compatible with `pymqi` while keeping the import name `pymqi`.

### Lazy loading

The IBM MQ client libraries are only loaded when a function requiring them is
first used (for example, on `QueueManager.connect`). This makes the source tree
safe for `python -m compileall` and avoids touching any native files during
import.

The upstream PyMQI sources are synchronized during the build process. See
[`scripts/sync_upstream.py`](scripts/sync_upstream.py) and the preserved license in
`LICENSE-THIRD-PARTY`.

## Quick build

To verify the source tree and produce distributable artifacts run:

```bash
python -m compileall
python setup.py sdist bdist_wheel
```

During the build the `setup.py` script downloads the upstream PyMQI release and
the IBM MQ Client runtime, bundling them into the resulting wheel. The setup
script also falls back to system locations such as `/usr/lib/python3/dist-packages`
to locate `setuptools` and `wheel` when they are not installed in the active
environment, so only the two commands above are needed on a networked machine.

## Build prerequisites

Install required system tools and Python build helpers (example for yum-based
distributions):

```bash
yum install -y gcc make curl tar rsync python3-setuptools python3-wheel
```

## Development

The project relies solely on `setuptools` for building and packaging. After
cloning the repository install it in editable mode:

```bash
python -m pip install -e .
```

### Synchronizing upstream PyMQI

To update the embedded PyMQI sources run:

```bash
PYMQI_VERSION=<version> python scripts/sync_upstream.py
```

The script downloads the specified PyMQI release, refreshes the contents of
`src/pymqi` and updates `LICENSE-THIRD-PARTY`.

### Running the linters and tests

The development tools such as `ruff`, `black`, `mypy` and `pytest` can be run
directly once installed in the environment. The tree also passes `python -m
compileall src/ tests/` to ensure there are no import-time side effects:

```bash
python -m compileall src tests
ruff src tests
black --check src tests
mypy src
pytest
```

## Building wheels

### Linux

The IBM MQ Client must be provided either by setting `MQ_INSTALLATION_PATH` or
by extracting it to `vendor/mq/` before building. The expected layout is:

```
vendor/mq/
    include/cmqc.h
    lib64/libmqic_r.so   # or lib/mqic_r.lib on Windows
```

### Linux

Run inside a `manylinux` container:

```bash
scripts/build_manylinux.sh
```

The script synchronizes the PyMQI sources, runs `python -m compileall src/
tests/` and downloads the IBM MQ client redistributable package (using a
default IBM link) to extract the required headers and libraries using
`genmqpkg.sh`. It then builds wheels for CPython 3.8–3.12 and repairs them with
`auditwheel`.

### Windows
Use the PowerShell script `scripts/build_windows.ps1` from a Visual Studio
Developer Command Prompt:

```powershell
./scripts/build_windows.ps1 -MqClientZipUrl <url>
```

The script runs `py -3 -m compileall src tests` and then builds wheels for
CPython 3.8–3.12. `delvewheel` is used to bundle the MQ runtime DLLs into the
final wheels.

## License

The Python sources are distributed under a proprietary license. The IBM MQ
Client remains covered by the IBM International Program License Agreement
(IPLA). Installing or using the IBM MQ Client indicates acceptance of the IBM
terms. The PyMQI sources are licensed under the BSD-3-Clause license preserved
in `LICENSE-THIRD-PARTY`.
