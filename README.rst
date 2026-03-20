==================
license-normaliser
==================

.. image:: https://raw.githubusercontent.com/barseghyanartur/license-normaliser/main/docs/_static/license_normaliser_logo.webp
   :alt: license-normaliser logo
   :align: center

Comprehensive license normalsation with a three-level hierarchy.

.. image:: https://img.shields.io/pypi/v/license-normaliser.svg
   :target: https://pypi.python.org/pypi/license-normaliser
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/license-normaliser.svg
   :target: https://pypi.python.org/pypi/license-normaliser/
   :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/license-normaliser/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/license-normaliser/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/license-normaliser/badge/?version=latest
    :target: http://license-normaliser.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/docs-llms.txt-blue
    :target: https://license-normaliser.readthedocs.io/en/latest/llms.txt
    :alt: llms.txt - documentation for LLMs

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/license-normaliser/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/license-normaliser/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/license-normaliser?branch=main
    :alt: Coverage

``license-normaliser`` is a comprehensive license normalisation library that
maps any license representation (SPDX tokens, URLs, prose descriptions) to a
canonical three-level hierarchy.

Features
========

- **Three-level hierarchy** - LicenseFamily → LicenseName → LicenseVersion.
- **Wide format support** - SPDX tokens, URLs, prose descriptions.
- **Creative Commons support** - Full CC family with versions and IGO variants.
- **Publisher-specific licenses** - Springer, Nature, Elsevier, Wiley, ACS,
  and more.
- **File-driven data** - Add aliases, URLs, and patterns by editing JSON files.
  No Python code changes required for new synonyms.
- **Pluggable data sources** - Drop in a new ``DataSource`` class to ingest
  any external license registry automatically.
- **Strict mode** - Raise ``LicenseNotFoundError`` instead of silently
  returning ``"unknown"``.
- **Caching** - LRU caching for performance.
- **CLI** - Command-line interface with ``--strict`` support.

Hierarchy
=========

The library uses a three-level hierarchy:

1. **LicenseFamily** - broad bucket: ``"cc"``, ``"osi"``, ``"copyleft"``,
   ``"publisher-tdm"``, ...
2. **LicenseName** - version-free: ``"cc-by"``, ``"cc-by-nc-nd"``, ``"mit"``,
   ``"wiley-tdm"``
3. **LicenseVersion** - fully resolved: ``"cc-by-3.0"``, ``"cc-by-nc-nd-4.0"``

Installation
============

With ``uv``:

.. code-block:: sh

    uv pip install license-normaliser

Or with ``pip``:

.. code-block:: sh

    pip install license-normaliser

Quick start
===========

.. code-block:: python
    :name: test_quick_start

    from license_normaliser import normalise_license

    v = normalise_license("CC BY-NC-ND 4.0")
    str(v)                  # "cc-by-nc-nd-4.0"   ← LicenseVersion
    str(v.license)          # "cc-by-nc-nd"       ← LicenseName
    str(v.license.family)   # "cc"                ← LicenseFamily

Strict mode
===========

By default, unresolvable inputs return an ``"unknown"`` result.  Pass
``strict=True`` to raise ``LicenseNotFoundError`` instead:

.. code-block:: python
    :name: test_strict_mode

    from license_normaliser import normalise_license
    from license_normaliser.exceptions import LicenseNotFoundError

    # Silent fallback (default)
    v = normalise_license("some-unknown-string")
    v.family.key  # "unknown"

    # Strict: raises on unresolvable input
    try:
        v = normalise_license("some-unknown-string", strict=True)
    except LicenseNotFoundError as exc:
        print(exc.raw)      # original input
        print(exc.cleaned)  # cleaned form that failed lookup

Batch normalisation
===================

.. code-block:: python
    :name: test_batch_normalisation

    from license_normaliser import normalise_licenses

    results = normalise_licenses(["MIT", "Apache-2.0", "CC BY 4.0"])
    for r in results:
        print(r.key)

    # Strict batch - raises on first unresolvable
    results = normalise_licenses(["MIT", "Apache-2.0"], strict=True)

Resolution pipeline (first match wins)
======================================

1. Direct registry lookup (cleaned lowercase key)
2. Alias table (loaded from ``data/aliases/aliases.json``)
3. Exact URL map (loaded from ``data/urls/url_map.json``)
4. Structural CC URL regex (any creativecommons.org URL not in the map)
5. Prose keyword scan (loaded from ``data/prose/prose_patterns.json``)
6. Fallback (key = cleaned string, family = unknown)

CLI usage
=========

Normalise a single license:

.. code-block:: sh

    license-normaliser normalise "MIT"
    # Output: mit

    license-normaliser normalise --full "CC BY 4.0"
    # Output:
    # Key: cc-by-4.0
    # URL: https://creativecommons.org/licenses/by/4.0/
    # License: cc-by
    # Family: cc

    license-normaliser normalise --strict "totally-unknown"
    # Exits with code 1 and prints an error

Batch normalise:

.. code-block:: sh

    license-normaliser batch MIT "Apache-2.0" "CC BY 4.0"
    license-normaliser batch --strict MIT "Apache-2.0"

Extending the data
==================

To add a new alias, URL mapping, or prose pattern **without touching Python**:

1. Edit the relevant JSON file in ``data/``.
2. Restart the Python process (the registry is built at import time).

See ``data/README.md`` for the full format specification and examples.

To add a brand-new license (with a new key):

1. Add entries to the JSON data files (``aliases.json``, ``url_map.json``, or
   ``prose_patterns.json``).  Each entry maps a key to a dict with
   ``version_key``, ``name_key``, and ``family_key``.
2. If the family is not covered by the regex fallback table
   in ``_registry.py``, add an explicit entry to ``aliases.json`` first.

To add an entirely new external data source:

1. Create ``src/license_normaliser/data_sources/my_source.py`` implementing
   the ``DataSource`` protocol.
2. Add it to ``REGISTERED_SOURCES`` in
   ``src/license_normaliser/data_sources/__init__.py``.

Exceptions
==========

.. code-block:: python
    :name: test_exceptions

    from license_normaliser.exceptions import (
        LicenseNormaliserError,   # base class
        LicenseNotFoundError,     # raised by strict mode
        DataSourceError,          # raised when a data file cannot be loaded
    )

Testing
=======

All tests run inside Docker:

.. code-block:: sh

    make test

To test a specific Python version:

.. code-block:: sh

    make test-env ENV=py312

License
=======

MIT

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
