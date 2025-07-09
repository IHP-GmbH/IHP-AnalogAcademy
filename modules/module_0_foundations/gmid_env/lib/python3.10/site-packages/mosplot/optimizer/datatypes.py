import numpy as np
from dataclasses import dataclass
from typing import Tuple, Literal, Union, List


@dataclass(frozen=True)
class Spec:
    """
    Target specification for a circuit parameter.

    Attributes:
        target: The target value.
        mode: "min" if lower values are preferred, "max" if higher values are preferred.
        weight: The cost weight for this specification.
    """

    target: float
    mode: Literal["min", "max"]
    weight: float

@dataclass(frozen=True)
class OptimizationParameter:
    """
    Represents an optimization parameter.

    Attributes:
        name: The parameter name.
        bound: A tuple, list, or 1D numpy array defining the lower and upper limits.
    """
    name: str
    bound: Union[Tuple[float, float], List[float], np.ndarray]
