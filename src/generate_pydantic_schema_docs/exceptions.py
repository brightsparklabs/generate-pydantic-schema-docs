"""
The Exceptions.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------

class GeneratePydanticSchemaDocsError(Exception):
    """Base exception for the application."""

class ModelDiscoveryError(GeneratePydanticSchemaDocsError):
    """Raised when Pydantic models cannot be discovered."""

class SchemaGenerationError(GeneratePydanticSchemaDocsError):
    """Raised when JSON Schema generation fails."""

class RenderingError(GeneratePydanticSchemaDocsError):
    """Raised when documentation rendering fails."""