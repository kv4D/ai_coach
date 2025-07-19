from typing import TypeVar, Iterable
from pydantic import BaseModel as PydanticModel
from db.models.base_model import BaseModel


# type parameter for Pydantic BaseModel children
TModel = TypeVar("TModel", bound=PydanticModel)
# type parameter for BaseModel children
TDBModel = TypeVar("TDBModel", bound=BaseModel)

def models_validate(model: type[TModel],
                          db_models: Iterable[TDBModel]) -> list[TModel] | None:
    """Convert database models to pydantic models.

    Args:
        model (type[TModel]): pydantic model
        db_models (Iterable[TDBModel] | TDBModel): database models

    Returns:
        list[TModel] | TModel | None: converted database models
    """
    if db_models is None:
        return None
    return [model.model_validate(m) for m in db_models]
