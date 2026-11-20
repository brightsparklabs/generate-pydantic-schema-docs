"""
Generate the JSON schemas from the pydantic models.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------

from typing import Any, Dict, List

from pydantic import BaseModel

from generate_pydantic_schema_docs.exceptions import SchemaGenerationError

# ------------------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------------------------


def generate_json_schema(
    models: List[type[BaseModel]], mode: str = "validation"
) -> Dict[str, Dict[str, Any]]:
    """Generate JSON schemas from the pydantic models.
    Save the JSON schemas to a temporary folder.

    Args:
        models: The pydantic models.
        mode: The mode to generate the schemas. Defaults to `validation`.
    """

    if models is None or models == []:
        return {}

    json_schemas = {}

    try:
        for model in models:
            json_schemas[model.__name__] = model.model_json_schema(mode=mode)
        return json_schemas
    except Exception as e:
        raise SchemaGenerationError(f"Could not generate JSON Schemas: {e}") from e
