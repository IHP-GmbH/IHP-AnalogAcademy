#!/usr/bin/env python3

import sys
from typing import Any, Dict, List, Tuple, TextIO


def _aggregate_sweep_data(sweep_list: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Aggregate individual sweep dictionaries into a single dictionary.

    Args:
        sweep_list: List of dictionaries, one per sweep.

    Returns:
        A dictionary with keys representing signal names and values as lists of sweep data.
    """
    aggregated_data: Dict[str, List[Any]] = {key: [] for key in sweep_list[0].keys()}
    for sweep in sweep_list:
        for key, value in sweep.items():
            aggregated_data[key].append(value)
    return aggregated_data


def _read_header(file: TextIO) -> Tuple[List[str], int, int, int]:
    """
    Read the file header and extract tokenized simulation parameters.

    Args:
        file: Open text file for reading.

    Returns:
        A tuple containing:
            - List of header tokens.
            - Number of automatic (independent) variables.
            - Number of probe variables.
            - Number of sweep parameters.
    """
    # Read the first line containing fixed-width counts
    header_line = file.readline()               # Example: contains info on variable counts
    num_auto = int(header_line[0:4])            # Number of automatic/independent variables
    num_probe = int(header_line[4:8])           # Number of probe variables
    num_sweep_params = int(header_line[8:12])   # Number of sweep parameters

    # Skip next two header lines (e.g. copyright info)
    file.readline()
    dataset_line = file.readline()
    # The last element in this line is the number of data sets (not used in this parser)
    _ = int(dataset_line.split()[-1])

    # Read the header line with simulation parameter names (may span multiple lines)
    simulation_header = file.readline()
    while '$&%#' not in simulation_header:
        simulation_header += file.readline()
    simulation_header = simulation_header.replace('\n', '')
    header_tokens: List[str] = simulation_header.split()[:-1]  # Discard the terminator token

    return header_tokens, num_auto, num_probe, num_sweep_params


def _clean_names(header_tokens: List[str], num_auto: int, num_probe: int) -> Tuple[List[str], List[str]]:
    """
    Extract and clean variable and parameter names from header tokens.

    Args:
        header_tokens: List of tokens from the simulation header.
        num_auto: Number of automatic (independent) variables.
        num_probe: Number of probe variables.
        num_sweep_params: Number of sweep parameters.

    Returns:
        A tuple containing:
            - Cleaned variable names.
            - Cleaned parameter names (prefixed with "param_").
    """
    # First tokens (data types) are not used.
    _unused_data_types: List[str] = header_tokens[0 : num_auto + num_probe]
    # Next tokens are the variable names.
    variable_names: List[str] = header_tokens[num_auto + num_probe : 2 * (num_auto + num_probe)]
    # Remaining tokens are parameter names.
    parameter_names: List[str] = header_tokens[2 * (num_auto + num_probe):]

    # Clean variable names by removing characters that may cause issues.
    variable_names = [
        token.partition('(')[0] if token.startswith('x') else token
        for token in variable_names
    ]
    variable_names = [token.replace('(', '_').replace('.', '_').replace(':', '_') for token in variable_names]

    # Clean parameter names and prepend 'param_'.
    parameter_names = [token.replace(':', '_') for token in parameter_names]
    parameter_names = ['param_' + token for token in parameter_names]

    return variable_names, parameter_names


def _read_sweep_data(file: TextIO, num_auto: int, num_probe: int, num_sweep_params: int,
                     variable_names: List[str], parameter_names: List[str]) -> List[Dict[str, Any]]:
    """
    Read sweep numeric data blocks until the end of file.

    Args:
        file: Open text file for reading.
        num_auto: Number of automatic (independent) variables.
        num_probe: Number of probe variables.
        num_sweep_params: Number of sweep parameters.
        variable_names: List of cleaned variable names.
        parameter_names: List of cleaned parameter names.

    Returns:
        A list of dictionaries, one for each sweep.
    """
    all_sweep_results: List[Dict[str, Any]] = []
    current_line = file.readline().strip()

    # Loop until there is no more data
    while current_line:
        # Initialize a new dictionary for this sweep with empty lists for each variable
        sweep_result: Dict[str, Any] = {name: [] for name in variable_names}
        # Initialize each parameter with a default value of 0
        for param in parameter_names:
            sweep_result[param] = 0

        sweep_numbers: List[float] = []
        # Determine the fixed field width (assumes scientific notation with 'E')
        field_width = current_line.find('E') + 4

        # Read the current sweep block until the terminator is encountered
        while True:
            last_row = '0.1000000E+31' in current_line
            while current_line:
                sweep_numbers.append(float(current_line[0:field_width]))
                current_line = current_line[field_width:]
            if last_row:
                break
            else:
                current_line = file.readline().strip()

        # Remove the terminator value from the sweep data
        sweep_numbers = sweep_numbers[:-1]
        # The first numbers are sweep parameters
        sweep_parameters = sweep_numbers[:num_sweep_params]

        # Extract data for each variable using slicing based on total columns (num_auto + num_probe)
        for index in range(len(variable_names)):
            sweep_result[variable_names[index]] = sweep_numbers[num_sweep_params + index :: num_auto + num_probe]

        # Add sweep parameters to the result dictionary (each as a single-item list)
        sweep_result.update(zip(parameter_names, [[value] for value in sweep_parameters]))
        all_sweep_results.append(sweep_result)

        # Read the next sweep block (if any)
        current_line = file.readline().strip()

    return all_sweep_results


def parse_file(file_path: str) -> Dict[str, List[Any]]:
    """
    Parse an ASCII Hspice output file and return the sweep data.

    Args:
        file_path: Path to the ASCII output file.

    Returns:
        A dictionary with keys for each signal and parameter; values are lists of simulation data.
    """
    with open(file_path, 'r') as file:
        header_tokens, num_auto, num_probe, num_sweep_params = _read_header(file)
        variable_names, parameter_names = _clean_names(header_tokens, num_auto, num_probe)
        sweep_data = _read_sweep_data(file, num_auto, num_probe, num_sweep_params, variable_names, parameter_names)
    return _aggregate_sweep_data(sweep_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hspice_parser.py <ascii_output_file>")
        sys.exit(1)
    input_file_path = sys.argv[1]
    parsed_data = parse_file(input_file_path)
    print(parsed_data.keys())
