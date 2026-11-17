"""
The CLI for the app.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------

from pathlib import Path

import typer

from generate_pydantic_schema_docs import (
    find_models, 
    generate_jinja2_context, 
    generate_json_schema, 
    render_ascii_docs,
)

# ------------------------------------------------------------------------------
# TYPER
# ------------------------------------------------------------------------------

app = typer.Typer(
    name="generate-pydantic-schema-docs",
    help="Generate AsciiDoc documentation from Pydantic models.",
    no_args_is_help=True,
)

@app.command()
def cli(
    module: str = typer.Option(..., help="Python module containing Pydantic models"),
    output: Path = typer.Option(..., help="Output AsciiDoc file"),
) -> None:
    """Generate AsciiDoc documentation from Pydantic models.

    Args:
        module:
        output:

    Raises:
        
    """

    output.mkdir(parents=True, exist_ok=True)

    # Find models in the python module.
    models = find_models(module)

    # Generate the JSON schemas.
    json_schema = generate_json_schema(models)

    # Generate the context for the jinja2.
    jinja2_context = generate_jinja2_context(json_schema)

    # Render the templates with the context.
    render_ascii_docs(jinja2_context, output)