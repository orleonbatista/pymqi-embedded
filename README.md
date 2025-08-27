# pymqi-embedded

`pymqi-embedded` embeds the [PyMQI](https://github.com/pymqi/pymqi) bindings for the IBM MQ
messaging system and bundles the IBM MQ Client runtime inside the wheel so that users do not
need a system wide installation of the MQ libraries.

## Features

- Works with Python 3.8 through 3.12.
- Linux wheels are built as `manylinux2014_x86_64` (or `manylinux_2_28_x86_64`).
- Windows wheels bundle the required DLLs using [delvewheel](https://github.com/adang1345/delvewheel).
- Pure Python API compatible with `pymqi` while keeping the import name `pymqi`.

The upstream PyMQI sources are synchronized during the build process. See
[`scripts/sync_upstream.sh`](scripts/sync_upstream.sh) and the preserved license in
`LICENSE-THIRD-PARTY`.

## Running

Install the package and use the included smoke test to check that the IBM MQ
Client libraries are correctly bundled:

```bash
python -m pip install .
export MQSERVER="host(port)/CHANNEL"
python scripts/smoke_test.py
```

The script connects to the queue manager defined by `MQSERVER` and accepts the
additional environment variables described in [Smoke test](#smoke-test) for an
optional put/get round trip.

## Development

The project relies solely on `setuptools` for building and packaging. After
cloning the repository install it in editable mode:

```bash
python -m pip install -e .
```

### Synchronizing upstream PyMQI

To update the embedded PyMQI sources run:

```bash
PYMQI_VERSION=<version> scripts/sync_upstream.sh
```

The script downloads the specified PyMQI release, refreshes the contents of
`src/pymqi` and updates `LICENSE-THIRD-PARTY`.

### Running the linters and tests

The development tools such as `ruff`, `black`, `mypy` and `pytest` can be run
directly once installed in the environment:

```bash
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
MQ_CLIENT_TAR_URL=<url to MQ client> scripts/build_manylinux.sh
```

The script synchronizes the PyMQI sources, downloads the IBM MQ client
redistributable package and extracts the required headers and libraries using
`genmqpkg.sh`. It then builds wheels for CPython 3.8–3.12 and repairs them with
`auditwheel`.

### Windows
Use the PowerShell script `scripts/build_windows.ps1` from a Visual Studio
Developer Command Prompt:

```powershell
./scripts/build_windows.ps1 -MqClientZipUrl <url>
```

`delvewheel` is used to bundle the MQ runtime DLLs into the final wheels.

### Smoke test

`scripts/smoke_test.py` connects to a queue manager and optionally performs a
put/get round trip. Required environment variables:

- `MQSERVER` – connection string in standard MQ format.
- `MQI_SMOKE_QMGR` – queue manager name (optional).
- `MQI_SMOKE_Q` – queue name for the optional put/get.
- `MQI_SMOKE_PUTGET=1` – enable the put/get round trip.

## License

The Python sources are distributed under a proprietary license. The IBM MQ
Client remains covered by the IBM International Program License Agreement
(IPLA). Installing or using the IBM MQ Client indicates acceptance of the IBM
terms. The PyMQI sources are licensed under the BSD-3-Clause license preserved
in `LICENSE-THIRD-PARTY`.
