"""Convenience type definitions for :mod:`bitex`'s type hints."""
# Built-in
from typing import Any, Dict, List, Tuple, Union

DecodedParams = Tuple[Tuple[str, List[Any]], ...]
RegexMatchDict = Dict[str, Union[str, None]]
Triple = Tuple[int, str, Union[str, int, float]]
KeyValuePairs = Dict[str, Union[str, int, float]]
