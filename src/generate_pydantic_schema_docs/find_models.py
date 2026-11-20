"""
Discovery of pydantic models.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------

import importlib
import inspect
from pathlib import Path
import sys

from pydantic import BaseModel

from generate_pydantic_schema_docs.exceptions import ModelDiscoveryError

# ------------------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------------------------


def import_package(module_name: str, module_path: Path):
    sys.path.insert(0, str(module_path))

    try:
        return importlib.import_module(module_name)
    finally:
        sys.path.insert(0, str(module_path))


def find_models(
    module_name: str,
    module_path: Path,
) -> list[type[BaseModel]]:
    """Discover Pydantic models defined in a Python module.

    Args:
        module_name: The python module to discover pydantic models from.
        selected_models: Option to select specific models to generate schema for. Defaults to None.

    Raises:
        ModelDiscoveryError: Raised when the module could not be imported, selected models are not
            found, or if no models are found.
    Returns:

    """
    # Try to import the module.
    try:
        module = import_package(module_name, module_path)
    except ImportError as e:
        raise ModelDiscoveryError(f"Could not import module '{module_name}': {e}") from e

    models = []
    modules = [module]

    module_path = module_path / module_name

    # Discover submodules if this is a package.
    for file_path in module_path.rglob("*.py"):
        relative_path = file_path.relative_to(module_path)

        # Skip test files and directories
        if any("test" in part.lower() for part in relative_path.parts):
            continue

        # Convert file path to Python module name
        parts = list(relative_path.with_suffix("").parts)

        if parts[-1] == "__init__":
            parts.pop()

        if not parts:
            continue
        print(relative_path)
        print(parts)

        submodule_name = f"{module_name}.{'.'.join(parts)}"

        try:
            print(submodule_name)
            submodule = importlib.import_module(submodule_name)
            modules.append(submodule)
        except ImportError:
            print(f"Could not import {submodule_name}")
            raise
    print("All modules:", modules)
    for current_module in modules:
        for _, obj in inspect.getmembers(current_module, inspect.isclass):
            print()
            print("Found OBJ:", obj)
            print("BaseModel", issubclass(obj, BaseModel))
            print(obj.__module__, current_module.__name__)
            print(obj.__module__ == current_module.__name__)
            if (
                issubclass(obj, BaseModel)
                and obj is not BaseModel
                and obj.__module__ == current_module.__name__
            ):
                models.append(obj)

    # If no models were found, throw and error.
    if models == []:
        raise ModelDiscoveryError(f"No Pydantic models found in '{module_name}'.")

    # Sort models.
    models = sorted(models, key=lambda model: model.__name__)

    return models
