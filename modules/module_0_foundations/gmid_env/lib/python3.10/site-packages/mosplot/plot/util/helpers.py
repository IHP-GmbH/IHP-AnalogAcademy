# imports <<<
from typing import Optional, Tuple

import numpy as np

from ..expressions import Expression
# >>>

def load_lookup_table(path: str) -> dict:
    return np.load(path, allow_pickle=True)["lookup_table"].item()

def evaluate_expression(expression: Expression, table: dict, filter_by_rows: Optional[np.ndarray] = None) -> Tuple[np.ndarray, str]:
    filter_by_rows = np.array([]) if filter_by_rows is None else filter_by_rows
    var_list = []
    for var in expression.variables:
        data = table[var]
        if filter_by_rows.size > 0 and data.ndim > 1:
            var_list.append(np.take(data, filter_by_rows, axis=0))
        else:
            var_list.append(data)
    result = (
        expression.function(*var_list)
        if expression.function is not None
        else var_list[0]
    )
    return result, expression.label
