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

from typing import Annotated
import typer

from generate_pydantic_schema_docs.find_models import find_models
from generate_pydantic_schema_docs.generate_jinja2_context import generate_jinja2_context
from generate_pydantic_schema_docs.generate_json_schema import generate_json_schema
from generate_pydantic_schema_docs.render_ascii_docs import render_ascii_docs

# ------------------------------------------------------------------------------
# TYPER
# ------------------------------------------------------------------------------

app = typer.Typer(
    name="generate-pydantic-schema-docs",
    help="Generate AsciiDoc documentation from Pydantic models.",
    no_args_is_help=True,
)


def generate_pydantic_schema_docs(
    module: str,
    module_path: Path,
    output: Path,
) -> None:
    """Generate AsciiDoc documentation from Pydantic models.

    Args:
        module: Python module to generate documents for.
        output: The output directory to write the docs to.
    """

    output.mkdir(parents=True, exist_ok=True)

    # Find models in the python module.
    module = module_path.name
    module_path = module_path.parent
    models = find_models(module, module_path)
    typer.echo(f"Found models: {models}")

    # Generate the JSON schemas.
    json_schema = generate_json_schema(models)
    typer.echo(f"Generated JSON Schemas: {json_schema}")

    # Generate the context for the jinja2.
    jinja2_context = generate_jinja2_context(json_schema)
    typer.echo(f"Jinja2 context: {jinja2_context}")

    # Render the templates with the context.
    render_ascii_docs(jinja2_context, output)


@app.command()
def cli(
    module: Annotated[
        str, typer.Option("--module", help="Python module containing Pydantic models")
    ],
    module_path: Annotated[Path, typer.Option("--module_path", help="Python module path.")],
    output: Annotated[Path, typer.Option("--output", help="Output AsciiDoc file")],
) -> None:
    """CLI entry point to generate AsciiDoc documentation from Pydantic models.

    Args:
        module: Python module to generate documents for.
        output: The output directory to write the docs to.
    """
    print(f"Module: {module}, type: {type(module)}")
    print(f"Output: {output}, type: {type(output)}")
    generate_pydantic_schema_docs(module, module_path, output)


if __name__ == "__main__":
    app()
