"""
The module type_defs contains additional type definitions used by the main repository.
"""

from importlib.resources.abc import Traversable
import os
import typing

# Typing hint Union for the different ways a file or data can be represented
DataInput: typing.TypeAlias = Traversable | os.PathLike[str] | str | typing.TextIO
