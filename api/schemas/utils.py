from typing import TypeVar, Iterable
from pydantic import BaseModel as PydanticModel
from db.models.base_model import BaseDatabaseModel


# type parameter for Pydantic BaseModel children
TModel = TypeVar("TModel", bound=PydanticModel)
# type parameter for BaseModel children
TDBModel = TypeVar("TDBModel", bound=BaseDatabaseModel)

def models_validate(model: type[TModel],
                    db_models: Iterable[TDBModel]) -> list[TModel]:
    """Convert database models to pydantic models.

    Args:
        model (type[TModel]): pydantic model
        db_models (Iterable[TDBModel]): database models

    Returns:
        list[TModel]: converted database models
    """
    return [model.model_validate(db_model) for db_model in db_models]
