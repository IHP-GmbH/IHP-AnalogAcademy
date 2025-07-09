# imports <<<
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np
import numpy.typing as npt
# >>>


def tile_arrays(A: npt.NDArray, B: npt.NDArray) -> Tuple[npt.NDArray, npt.NDArray]:
    if A.ndim == 1 and B.ndim == 2:
        if A.shape[0] == B.shape[0]:
            return np.tile(A, (B.shape[1], 1)).T, B
        elif A.shape[0] == B.shape[1]:
            return np.tile(A, (B.shape[0], 1)), B
    elif B.ndim == 1 and A.ndim == 2:
        if B.shape[0] == A.shape[0]:
            return A, np.tile(B, (A.shape[1], 1)).T
        elif B.shape[0] == A.shape[1]:
            return A, np.tile(B, (A.shape[0], 1))
    return A, B

def extract_2d_table(
    lookup_table: dict,
    length: Optional[Union[float, list, npt.NDArray]] = None,
    vbs: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
    vgs: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
    vds: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
    primary: Optional[str] = None,
    parameters: Optional[list] = None,
) -> Tuple[Optional[str], Dict, dict]:
    # Ensure at least two sweep parameters are provided.
    if sum(param is not None for param in [length, vbs, vgs, vds]) < 2:
        raise ValueError("Provide at least two parameters.")

    def process_target(data: np.ndarray, target, var_name: str):
        if isinstance(target, tuple):

            if len(target) < 2:
                raise ValueError("Target tuple must have at least start and stop values.")

            start_val, stop_val = target[0], target[1]
            ascending = start_val <= stop_val

            # Find the indices in data closest to start and stop.
            start_idx = int(np.abs(data - start_val).argmin())
            stop_idx = int(np.abs(data - stop_val).argmin())

            # Ensure indices are in the correct order.
            if ascending and start_idx > stop_idx:
                start_idx, stop_idx = stop_idx, start_idx
            elif not ascending and start_idx < stop_idx:
                start_idx, stop_idx = stop_idx, start_idx

            # Build a continuous index sequence that includes both start and stop.
            if ascending:
                inds = np.arange(start_idx, stop_idx + 1)
            else:
                inds = np.arange(start_idx, stop_idx - 1, -1)

            # If a step is specified, sample every step element.
            if len(target) == 3:
                step_val = target[2]

                if len(data) < 2:
                    raise ValueError("Data must have at least two elements to determine spacing.")

                # Assume uniform spacing.
                dx = data[1] - data[0] if data[0] <= data[-1] else data[-2] - data[-1]
                index_step = int(round(abs(step_val) / dx))
                if index_step == 0:
                    raise ValueError("Step value is too small compared to data spacing.")
                step_idx = index_step if ascending else -index_step
                sliced_inds = inds[::step_idx]

                # Always include the final element.
                if sliced_inds[-1] != inds[-1]:
                    sliced_inds = np.concatenate((sliced_inds, [inds[-1]]))
                inds = sliced_inds

            return inds, data[inds], False

        if var_name == "length" and isinstance(target, (list, np.ndarray)):
            target_arr = np.array(target)
            mask = np.isin(data, target_arr)
            inds = np.nonzero(mask)[0]
            return inds, data[inds], False

        idx = int(np.abs(data - target).argmin())
        return np.array([idx]), data[idx], True

    # Slice a 4D array using indices for each axis.
    def apply_slice(a: npt.NDArray, slices: Tuple) -> npt.NDArray:
        s = a[slices[0], :, :, :]
        s = s[:, slices[1], :, :]
        s = s[:, :, slices[2], :]
        s = s[:, :, :, slices[3]]
        return s

    sweep_params = {"length": length, "vbs": vbs, "vgs": vgs, "vds": vds}
    indices_dict = {}
    values_dict = {}
    is_scalar = {}

    for var, target in sweep_params.items():
        if target is None:
            indices_dict[var] = slice(None)
            values_dict[var] = lookup_table[var]
            is_scalar[var] = False
        else:
            inds, vals, scalar_flag = process_target(lookup_table[var], target, var)
            indices_dict[var] = inds
            values_dict[var] = vals
            is_scalar[var] = scalar_flag

    # Determine the secondary sweep variable.
    secondary = None
    if primary:
        if sweep_params.get(primary) is None:
            raise ValueError("Primary variable must be provided.")
        non_primary_ranges = [var for var in sweep_params if var != primary and not is_scalar[var]]
        if len(non_primary_ranges) == 1:
            secondary = non_primary_ranges[0]
        elif len(non_primary_ranges) > 1:
            for var in ["length", "vbs", "vgs", "vds"]:
                if var != primary and var in non_primary_ranges:
                    secondary = var
                    break

    slice_indices = (
        indices_dict["length"],
        indices_dict["vbs"],
        indices_dict["vgs"],
        indices_dict["vds"],
    )
    filter_values = {
            "length": values_dict["length"],
            "vbs": values_dict["vbs"],
            "vgs": values_dict["vgs"],
            "vds": values_dict["vds"],
    }


    if parameters is None:
        parameters = lookup_table.get("parameter_names", [])

    # Precompute keys with 4D data.
    keys_4d = [p for p in parameters if p in lookup_table and lookup_table[p].ndim == 4]
    if not keys_4d:
        raise ValueError("No parameter with 4 dimensions found for tiling.")
    reference_key = keys_4d[0]

    extracted_table = {}
    for p in parameters:
        if p not in lookup_table:
            continue
        data = lookup_table[p]
        if p in keys_4d:
            data = np.squeeze(apply_slice(data, slice_indices))
        if data.ndim > 1 and data.shape[0] > data.shape[1]:
            data = data.T
        extracted_table[p] = data

    for var in ["length", "vbs", "vgs", "vds"]:
        extracted_table[var], _ = tile_arrays(values_dict[var], extracted_table[reference_key])

    return secondary, filter_values, extracted_table
