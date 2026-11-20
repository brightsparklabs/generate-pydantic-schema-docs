"""
Renders ASCII docs from jinja2 context.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------

from pathlib import Path
from typing import Any, Dict
from jinja2 import Environment, FileSystemLoader

# ------------------------------------------------------------------------------
# PUBLIC FUNCTION
# ------------------------------------------------------------------------------


def render_ascii_docs(jinja2_context: Dict[str, Dict[str, Any]], output: Path) -> None:
    """Generate individual AsciiDoc files and an index for a module.

    Args:
        jinja2_context: The jinja2 context.
    """

    template_dir = Path(__file__).parent / "templates"

    environment = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )

    generated_files = []

    # Generate individual model documentation.
    for model_name, model_context in jinja2_context.items():
        template = environment.get_template("schema.adoc.j2")

        output_path = output / f"{model_name.lower()}.adoc"
        output_path.write_text(
            template.render(**model_context),
            encoding="utf-8",
        )

        generated_files.append(output_path)

    return generated_files
