import logging
import os
import inspect
import pathlib
from collections.abc import Generator


def get_libs():
    libs: list = []

    path: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    lib_directory: Generator[pathlib.Path, None, None] = pathlib.Path(path).rglob("*.py")

    for file in lib_directory:
        if file.name == "__init__.py":
            continue
        module_name = file.name.split(".")[0]
        logging.debug("Found '{0}' in '{1}'".format(module_name, path))
        libs.append(module_name)

    return libs


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_libs()
