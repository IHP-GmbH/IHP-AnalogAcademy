from typing import Callable, List, Any, Optional


class Expression:
    def __init__(
        self,
        variables: List[str],
        label: str = "",
        function: Optional[Callable[..., Any]] = None,
    ) -> None:
        self.variables = variables
        self.label = label
        self.function = (
            function
            if function is not None
            else (lambda *x: x[0] if len(x) == 1 else x)
        )
