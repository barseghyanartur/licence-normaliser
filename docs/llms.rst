Project source-tree
===================

Below is the layout of the project (to 10 levels), followed by
the contents of each key file.

.. code-block:: text
   :caption: Project directory layout

   license-normaliser/
   ├── src
   │   └── license_normaliser
   │       ├── cli
   │       │   ├── __init__.py
   │       │   └── _main.py
   │       ├── tests
   │       │   ├── __init__.py
   │       │   ├── conftest.py
   │       │   ├── test_cli.py
   │       │   └── test_core.py
   │       ├── __init__.py
   │       ├── _core.py
   │       ├── _enums.py
   │       └── py.typed
   ├── AGENTS.md
   ├── conftest.py
   ├── CONTRIBUTING.rst
   ├── docker-compose.yml
   ├── Dockerfile
   ├── Makefile
   ├── pyproject.toml
   ├── README.rst
   ├── tox.ini
   └── uv.lock

README.rst
----------

.. literalinclude:: ../README.rst
   :language: rst
   :caption: README.rst

CONTRIBUTING.rst
----------------

.. literalinclude:: ../CONTRIBUTING.rst
   :language: rst
   :caption: CONTRIBUTING.rst

AGENTS.md
---------

.. literalinclude:: ../AGENTS.md
   :language: markdown
   :caption: AGENTS.md

conftest.py
-----------

.. literalinclude:: ../conftest.py
   :language: python
   :caption: conftest.py

docker-compose.yml
------------------

.. literalinclude:: ../docker-compose.yml
   :language: yaml
   :caption: docker-compose.yml

pyproject.toml
--------------

.. literalinclude:: ../pyproject.toml
   :language: toml
   :caption: pyproject.toml

src/license_normaliser/__init__.py
----------------------------------

.. literalinclude:: ../src/license_normaliser/__init__.py
   :language: python
   :caption: src/license_normaliser/__init__.py

src/license_normaliser/_core.py
-------------------------------

.. literalinclude:: ../src/license_normaliser/_core.py
   :language: python
   :caption: src/license_normaliser/_core.py

src/license_normaliser/_enums.py
--------------------------------

.. literalinclude:: ../src/license_normaliser/_enums.py
   :language: python
   :caption: src/license_normaliser/_enums.py

src/license_normaliser/cli/__init__.py
--------------------------------------

.. literalinclude:: ../src/license_normaliser/cli/__init__.py
   :language: python
   :caption: src/license_normaliser/cli/__init__.py

src/license_normaliser/cli/_main.py
-----------------------------------

.. literalinclude:: ../src/license_normaliser/cli/_main.py
   :language: python
   :caption: src/license_normaliser/cli/_main.py

src/license_normaliser/tests/__init__.py
----------------------------------------

.. literalinclude:: ../src/license_normaliser/tests/__init__.py
   :language: python
   :caption: src/license_normaliser/tests/__init__.py

src/license_normaliser/tests/conftest.py
----------------------------------------

.. literalinclude:: ../src/license_normaliser/tests/conftest.py
   :language: python
   :caption: src/license_normaliser/tests/conftest.py

src/license_normaliser/tests/test_cli.py
----------------------------------------

.. literalinclude:: ../src/license_normaliser/tests/test_cli.py
   :language: python
   :caption: src/license_normaliser/tests/test_cli.py

src/license_normaliser/tests/test_core.py
-----------------------------------------

.. literalinclude:: ../src/license_normaliser/tests/test_core.py
   :language: python
   :caption: src/license_normaliser/tests/test_core.py
