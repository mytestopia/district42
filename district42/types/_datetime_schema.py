from datetime import datetime
from typing import Any

from niltype import Nil, Nilable
from typing_extensions import TypeAlias

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import make_already_declared_error, make_invalid_type_error
from ._schema import Schema

__all__ = ("DateTimeSchema", "DateTimeProps",)


class DateTimeProps(Props):
    @property
    def value(self) -> Nilable[datetime]:
        return self.get("value")


class DateTimeSchema(Schema[DateTimeProps]):
    type: TypeAlias = str

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_datetime(self, **kwargs)

    def __call__(self, /, value: datetime) -> "DateTimeSchema":
        if not isinstance(value, datetime):
            raise make_invalid_type_error(self, value, (datetime,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))
