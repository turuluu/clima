Example project to showcase clima
---------------------------------

The command `my_tool` is defined in `pyproject.toml` (see "scripts"). The cli object is wrapped when the file
`the_tool.py` is imported in to `__init__.py` - or rather - to the module.

In other words, the main is refered to just as placeholder:

**my_tool/__init__.py**
    .. code-block::

        from my_tool.the_tool import main as main_tool

**pyproject.toml**
    .. code-block::

        [tool.poetry.scripts]
        my_tool = "my_tool:main_tool"

**my_tool/the_tool.py**
    .. code-block::

        def main():
            pass

To run this project, install poetry and run:

.. code-block::

    pip install poetry
    poetry install
    poetry run my_tool
