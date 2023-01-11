#!/usr/bin/env python3
""" a type-annotated function make_multiplier """
from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''
    Annotate the below function’s
    parameters and return
    values with the appropriate types
    '''
    return [(i, len(i)) for i in lst]
