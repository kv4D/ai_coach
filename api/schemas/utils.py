"""Extra functions for schemas."""
from typing import TypeVar, Iterable
from pydantic import BaseModel as PydanticModel
from database.base_model import BaseDatabaseModel


# type parameter for Pydantic BaseModel children
SchemaT = TypeVar("SchemaT", bound=PydanticModel)
# type parameter for BaseModel children
DatabaseModelT = TypeVar("DatabaseModelT", bound=BaseDatabaseModel)


def models_validate(model: type[SchemaT],
                    db_models: Iterable[DatabaseModelT]) -> list[SchemaT]:
    """Convert database models to pydantic models.

    Args:
        model (type[SchemaT]): pydantic model
        db_models (Iterable[DatabaseModelT]): database models

    Returns:
        list[SchemaT]: converted database models
    """
    return [model.model_validate(db_model) for db_model in db_models]
