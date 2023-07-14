"""Base types used in Connex."""

from pydantic import BaseModel


def to_camel(string: str) -> str:
    """Converter for variables from snake_case to camelCase.

    Args:
        string (str): the variable to convert to camelCase.

    Returns:
        str: camelCase representation of the variable.
    """
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelModel(BaseModel):
    """Converting snake_case pydantic models to camelCase models."""

    class Config:
        """Configuration for a camelCase based model conversion."""

        alias_generator = to_camel
        allow_population_by_field_name = True
