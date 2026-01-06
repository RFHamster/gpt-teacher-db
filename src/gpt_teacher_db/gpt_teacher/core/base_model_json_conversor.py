from typing import List, Type, TypeVar, Union, get_args, get_origin

from pydantic import BaseModel
from sqlalchemy import JSON as SQLAlchemyJSON
from sqlalchemy.types import TypeDecorator
from sqlmodel import Column, Field

T = TypeVar("T", bound=BaseModel)


class PydanticJSONType(TypeDecorator):
    """
    Tipo SQLAlchemy customizado (https://docs.sqlalchemy.org/en/20/core/custom_types.html)
    que converte automaticamente entre BaseModel/List[BaseModel] e JSON
    """

    impl = SQLAlchemyJSON
    cache_ok = True

    def __init__(self, pydantic_type: Union[Type[BaseModel], Type[List[BaseModel]]]):
        self.pydantic_type = pydantic_type
        self.is_list = get_origin(pydantic_type) is list
        if self.is_list:
            self.item_type = get_args(pydantic_type)[0]
        else:
            self.item_type = pydantic_type

        super().__init__()

    def process_bind_param(self, value, dialect):
        """
        Converte um valor, esperado ser BaseModel/List[BaseModel], para dict/list ao salvar no banco.
        Caso o valor de entrada não for BaseModel/List[BaseModel], sua conversão é None.
        """
        if value is None:
            return None

        if self.is_list:
            if isinstance(value, list):
                return [
                    item.model_dump() if isinstance(item, BaseModel) else item
                    for item in value
                ]
            return []
        else:
            if isinstance(value, BaseModel):
                return value.model_dump()
            if isinstance(value, dict):
                return value

        return None

    def process_result_value(self, value, dialect):
        """Converte o valor salvo no banco (dict/list) para BaseModel/List[BaseModel]"""
        if value is None:
            return None

        if self.is_list:
            if isinstance(value, list):
                try:
                    return [
                        self.item_type.model_validate(item)
                        if isinstance(item, dict)
                        else item
                        for item in value
                    ]
                except Exception:
                    return []
            return []
        else:
            if isinstance(value, dict):
                try:
                    return self.item_type.model_validate(value)
                except Exception:
                    return self.item_type()

        return value


def PydanticField(
    pydantic_type: Union[Type[T], Type[List[T]]], **kwargs
) -> Union[T, List[T]]:
    """Factory function para criar campos que convertem automaticamente entre BaseModel/List[BaseModel] e JSON"""
    if get_origin(pydantic_type) is list:
        default_factory = list
    else:
        default_factory = pydantic_type

    return Field(
        default_factory=default_factory,
        sa_column=Column(PydanticJSONType(pydantic_type)),
        **kwargs,
    )
