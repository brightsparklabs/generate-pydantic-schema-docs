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
from types import ModuleType
from typing import List

from pydantic import BaseModel

from generate_pydantic_schema_docs.exceptions import ModelDiscoveryError

# ------------------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------------------------


def _import_package(module_path: Path) -> ModuleType:
    """Imports the root python module from the module path.

    Args:
        module_path: The module path.

    Returns:
        The root python module.
    """
    sys.path.insert(0, str(module_path.parent.absolute()))
    try:
        return importlib.import_module(module_path.name)
    finally:
        sys.path.insert(0, str(module_path.parent.absolute()))


def _discover_modules(module_path: Path) -> list[ModuleType]:
    """Discovers the python modules from a module path.

    Args:
        module_path: The path directory where the python module is located.

    Raises:
        ModelDiscoveryError: Raised when the module could not be imported.
        RuntimeError: If there were any modules which could not be correctly imported.

    Returns:
        The modules which were imported.
    """
    module_name = module_path.name
    # Try to import the module.
    try:
        module = _import_package(module_path)
    except ImportError as e:
        raise ModelDiscoveryError(f"Could not import module '{module_name}': {e}") from e

    modules = [module]

    module_import_errors = []

    # Discover submodules if this is a package.
    for file_path in module_path.rglob("*.py"):
        relative_path = file_path.relative_to(module_path)

        if "test" in str(relative_path).lower():
            continue

        parts = relative_path.with_suffix("").parts

        if parts[-1] == "__init__":
            parts = parts[:-1]

        if parts == [] or parts is None:
            continue

        submodule_name = f"{module_name}.{'.'.join(parts)}"

        try:
            submodule = importlib.import_module(submodule_name)
            modules.append(submodule)
        except ImportError:
            module_import_errors.append(submodule_name)

    if module_import_errors != []:
        raise RuntimeError(f"Could not import the following submodules: {module_import_errors}")

    return modules


def _discover_models(modules: list[ModuleType]) -> List[type[object]]:
    """Find all the pydantic models in a list of python modules.

    Args:
        modules: The python modules found.

    Raises:
        ModelDiscoveryError: Raise if no pydantic models were found.

    Returns:
        The list of pydantic models found.
    """
    models = []
    # Find all the pydantic models.
    for current_module in modules:
        for _, obj in inspect.getmembers(current_module, inspect.isclass):
            if (
                issubclass(obj, BaseModel)
                and obj is not BaseModel
                and obj.__module__ == current_module.__name__
            ):
                models.append(obj)

    # If no models were found, throw and error.
    if models == []:
        raise ModelDiscoveryError("No Pydantic models found.")

    # Sort models.
    return sorted(models, key=lambda model: model.__name__)


def find_models(
    module_path: Path,
) -> list[type[BaseModel]]:
    """Discover Pydantic models defined in a Python module.

    Args:
        module_path: The path containing the python module.

    Returns:
        The list of pydantic models found.
    """

    modules = _discover_modules(module_path)

    models = _discover_models(modules)

    return models
