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

from pydantic import BaseModel

from generate_pydantic_schema_docs.exceptions import ModelDiscoveryError

# ------------------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------------------------

def find_models(
    module_name: str,
    selected_models: list[str] | None = None,
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
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise ModelDiscoveryError(f"Could not import module '{module_name}': {e}") from e

    models = []
    for _, object in inspect.getmembers(module, inspect.isclass):
        # The last condition is to make sure that we are only getting the models which are defined 
        # in the current module.
        if (
            issubclass(object, BaseModel) and 
            object is not BaseModel and 
            object.__module__ == module.__name__
        ):
            models.append(object)

    # Filter out the selected models from the discovered models.
    if selected_models is not None:
        model_map = {
            model.__name__: model
            for model in models
        }

        # If any of the selected models were not found, throw an error.
        missing = set(selected_models) - set(model_map)
        if missing:
            raise ModelDiscoveryError(
                f"Models not found in '{module_name}': "
                f"{', '.join(sorted(missing))}"
            )

        models = [
            model_map[name]
            for name in selected_models
        ]

    # If no models were found, throw and error.
    if models is []:
        raise ModelDiscoveryError(
            f"No Pydantic models found in '{module_name}'."
        )

    # Sort models.
    models = sorted(models, key=lambda model: model.__name__)

    return models