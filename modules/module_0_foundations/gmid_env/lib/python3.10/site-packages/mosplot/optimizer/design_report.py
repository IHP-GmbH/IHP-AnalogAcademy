from typing import Any, Dict, List, Optional
from .optimizer import Optimizer


class DesignReport:
    """
    Generates a design report for the optimized circuit.

    Attributes:
        circuit: The circuit object.
        optimizer: The Optimizer object used for optimization.
        opt_params: The optimal parameters obtained from the optimizer.
        full_specs: The circuit specifications evaluated at the optimal parameters.
        objective: The objective cost value from the optimizer's result.
    """

    def __init__(self, circuit: Any, optimizer: Optimizer) -> None:
        self.circuit = circuit
        self.optimizer = optimizer
        self.opt_params: Dict[str, float] = optimizer.get_opt_params()
        self.full_specs: Dict[str, Any] = circuit.evaluate_specs(**self.opt_params)
        self.objective: Optional[float] = (optimizer.result.fun if optimizer.result is not None else None)

    @staticmethod
    def format_eng(value: Optional[float]) -> str:
        """
        Formats an electrical value using engineering units.

        Args:
            value: The value to format.

        Returns:
            A string with the formatted value.
        """
        if value is None:
            return "N/A"
        if value < 1e-6:
            return f"{int(round(value * 1e9))}n"
        return f"{value * 1e6:.2f}u"

    @staticmethod
    def format_area(value: Optional[float]) -> str:
        """
        Formats an area value.

        Args:
            value: The area value in m².

        Returns:
            A string with the area formatted in µm² or nm².
        """
        if value is None:
            return "N/A"
        area_um2 = value * 1e12
        if area_um2 < 1:
            area_nm2 = value * 1e18
            return f"{area_nm2:.3f} nm²"
        return f"{area_um2:.3f} um²"

    def report(self) -> str:
        """
        Generates a detailed design report.

        Returns:
            A multi-line string with transistor details and final circuit specifications.
        """
        lines: List[str] = []
        dims = getattr(self.circuit, "device_dimensions", None)
        lines.append("\nTransistor Details:")
        if dims:
            for device, item in dims.items():
                lines.append(f"    {device}:")
                length = item.get("Length")
                width = item.get("Width")
                area = item.get("Area")
                current = item.get("Current")
                gmid = item.get("GMID")
                lines.append(f"        Length: {self.format_eng(length)}")
                lines.append(f"        Width: {self.format_eng(width)}")
                lines.append(f"        Area: {self.format_area(area)}")
                lines.append(f"        Current: {self.format_eng(current)}")
                if gmid is not None:
                    lines.append(f"        GmID: {gmid:.2f}")
        else:
            lines.append("    Not available.")

        lines.append("\nFinal Circuit Specs:")
        if self.full_specs:
            for key, val in self.full_specs.items():
                if key == "Area":
                    lines.append(f"    {key}: {self.format_area(val)}")
                else:
                    try:
                        lines.append(f"    {key}: {val:.4g}")
                    except (ValueError, TypeError):
                        lines.append(f"    {key}: {val}")
        else:
            lines.append("    Not available.")
        return "\n".join(lines)
