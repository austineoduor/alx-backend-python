#!/usr/bin/env python3
""" a type-annotated function safely_get_value """
from typing import Union, Any, Mapping, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None]) -> Union[Any, T]:
    """ function safely_get_value """
    if key in dct:
        return dct[key]
    else:
        return default
