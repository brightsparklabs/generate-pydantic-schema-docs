"""
Generate the Jinja2 context from the JSON schemas.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------

from typing import Any, Dict

# ------------------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------------------------


def generate_jinja2_context(json_schemas: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Convert the json schemas to a jinja2 context.

    Args:
        json_schemas: JSON schemas of the pydantic models.

    Returns:
        The context for the jinja2 template.
    """

    contexts = {}

    for model_name, json_schema in json_schemas.items():
        required = set(json_schema.get("required", []))
        fields = []

        for field_name, prop in json_schema.get("properties", {}).items():
            fields.append(
                {
                    "name": field_name,
                    "required": field_name in required,
                    "description": prop.get("description", ""),
                }
            )

        contexts[model_name] = {
            "title": json_schema.get("title", model_name),
            "description": json_schema.get("description", ""),
            "fields": fields,
        }

    return contexts
