"""
Generate the JSON schemas from the pydantic models.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------

from typing import Any

from pydantic import BaseModel, ConfigDict

from generate_pydantic_schema_docs.exceptions import SchemaGenerationError

# ------------------------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------------------------


def _enable_attribute_docstrings(
    models: list[type[BaseModel]],
) -> None:
    """
    Enable attribute docstrings for discovered models.

    Args:
        models: A list of pydantic models.
    """

    for model in models:
        model.model_config = ConfigDict(
            **model.model_config,
            use_attribute_docstrings=True,
        )
        model.model_rebuild(force=True)


def generate_json_schema(
    models: list[type[BaseModel]], mode: str = "validation"
) -> dict[str, dict[str, Any]]:
    """Generate JSON schemas from the pydantic models.
    Save the JSON schemas to a temporary folder.

    Args:
        models: The pydantic models.
        mode: The mode to generate the schemas. Defaults to `validation`.
    """
    # Enable the docstrings to be included when json schemas are generated.
    _enable_attribute_docstrings(models)

    if models is None or models == []:
        return {}

    json_schemas = {}

    try:
        for model in models:
            json_schemas[model.__name__] = model.model_json_schema(mode=mode)
        return json_schemas
    except Exception as e:
        raise SchemaGenerationError(f"Could not generate JSON Schemas: {e}") from e
