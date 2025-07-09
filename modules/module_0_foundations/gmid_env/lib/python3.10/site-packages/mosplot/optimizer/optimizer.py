from typing import Any, Dict, List, Optional
import numpy as np
from scipy.optimize import OptimizeResult, differential_evolution
from .datatypes import OptimizationParameter, Spec


class Optimizer:
    """
    Optimizes a circuit design using differential evolution.

    Attributes:
        circuit: The circuit object with an evaluate_specs method.
        parameters: A list of OptimizationParameter objects.
        target_specs: A dictionary mapping spec names to Spec objects.
        opt_params: The optimal parameters found after optimization.
        result: The optimization result from differential evolution.
    """

    def __init__(
        self,
        circuit: Any,
        parameters: List[OptimizationParameter],
        target_specs: Dict[str, Spec],
    ) -> None:
        self.circuit = circuit
        self.parameters = parameters
        self.target_specs = target_specs
        self.opt_params: Optional[Dict[str, float]] = None
        self.result: Optional[OptimizeResult] = None

    @staticmethod
    def compute_cost(specs: Dict[str, float], target_specs: Dict[str, Spec]) -> float:
        """
        Computes the cost based on actual circuit specifications and target specifications.

        Args:
            specs: A dictionary of actual circuit specifications.
            target_specs: A dictionary mapping specification names to Spec objects.

        Returns:
            The computed cost as a float.
        """
        cost = 0.0
        for key, spec_target in target_specs.items():
            target = spec_target.target
            mode = spec_target.mode
            weight = spec_target.weight
            actual = specs[key]
            error = 0.0
            if mode == "min":
                error = max(0, (actual - target) / target)
            elif mode == "max" and actual < target:
                error = max(0, (target - actual) / target)
            cost += weight * (error**2)
        return cost

    def _transform_params(self, x: List[float]) -> Dict[str, float]:
        """
        Transforms optimizer variables into actual parameter values.
        Handles continuous and discrete bounds.
        """
        params: Dict[str, float] = {}
        for i, param in enumerate(self.parameters):
            bound = param.bound
            if isinstance(bound, (list, np.ndarray)):
                # Discrete parameter: x is an index in [0, len(bound)-1]
                idx = int(round(x[i]))
                idx = max(0, min(idx, len(bound) - 1))
                params[param.name] = float(np.array(bound)[idx])
            else:
                # Continuous parameter
                params[param.name] = x[i]
        return params

    def _objective(self, x: List[float]) -> float:
        """
        Objective function for optimization.

        Args:
            x: A list of optimizer variables.

        Returns:
            The cost computed for the given parameter values.
        """
        params = self._transform_params(x)
        specs = self.circuit.evaluate_specs(**params)
        return self.compute_cost(specs, self.target_specs)

    def optimize(self, maxiter: int = 10) -> OptimizeResult:
        """
        Runs the differential evolution optimization.

        Args:
            maxiter: Maximum number of iterations for the optimizer (default: 10).

        Returns:
            The optimization result.
        """
        bounds = []
        for param in self.parameters:
            bound = param.bound
            if isinstance(bound, (list, np.ndarray)):
                # Discrete parameter: search index range
                bounds.append((0, len(bound) - 1))
            else:
                bounds.append(bound)

        self.result = differential_evolution(
            self._objective,
            bounds,
            disp=True,
            maxiter=maxiter,
            polish=True
        )

        # Decode optimal parameters from result.x
        opt_params: Dict[str, float] = {}
        for i, param in enumerate(self.parameters):
            bound = param.bound
            if isinstance(bound, (list, np.ndarray)):
                idx = int(round(self.result.x[i]))
                idx = max(0, min(idx, len(bound) - 1))
                opt_params[param.name] = float(np.array(bound)[idx])
            else:
                opt_params[param.name] = self.result.x[i]

        self.opt_params = opt_params
        return self.result

    def get_opt_params(self) -> Dict[str, float]:
        """
        Returns the optimal parameters found after optimization.

        Returns:
            A dictionary of optimal parameters.
        """
        if self.opt_params is None:
            raise ValueError("Optimization has not been performed yet.")
        return self.opt_params

