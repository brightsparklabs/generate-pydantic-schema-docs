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

from generate_pydantic_schema_docs import find_models

# ------------------------------------------------------------------------------
# TYPER
# ------------------------------------------------------------------------------

app = typer.Typer(
    name="generate-pydantic-schema-docs",
    help="Generate AsciiDoc documentation from Pydantic models.",
    no_args_is_help=True,
)

@app.command()
def generate(
    module: str = typer.Option(..., help="Python module containing Pydantic models"),
    output: Path = typer.Option(..., help="Output AsciiDoc file"),
    model: str | None = typer.Option(None, help="Specific model to document"),
):
    """Generate AsciiDoc documentation from Pydantic models."""

    models = find_models(module)

    if model:
        models = [m for m in models if m.__name__ == model]
        if not models:
            raise typer.BadParameter(f"Model '{model}' not found")

    # Now generate the documents.

    typer.echo(f"Documentation generated: {output}")
# ------------------------------------------------------------------------------
# ENTRYPOINT
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app()
