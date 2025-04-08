import re
import sys
import os



def parse_verilog(verilog_file):
    """Extract module name, inputs, and outputs from a Verilog file while expanding bus signals."""
    with open(verilog_file, "r") as f:
        code = f.read()

    module_match = re.search(r"module\s+(\w+)\s*\(", code)
    if not module_match:
        raise ValueError("No module found in the Verilog file.")
    module_name = module_match.group(1)

    # Remove comments
    code = re.sub(r"//.*", "", code)

    # Adjusted regex to capture bus definitions properly
    ports = re.findall(r"(input|output)\s*(?:wire|reg)?\s*(\[\d+:\d+\])?\s*(\w+)", code)

    inputs = []
    outputs = []
    for direction, bus, name in ports:
        if bus:
            # Extract bus range
            msb, lsb = map(int, re.findall(r"\d+", bus))
            indices = range(msb, lsb - 1, -1) if msb >= lsb else range(msb, lsb + 1)
            expanded_names = [f"{name}{i}" for i in indices]  # Adjusted naming convention
        else:
            expanded_names = [name]

        if direction == "input":
            inputs.extend(expanded_names)
        else:
            outputs.extend(expanded_names)

    # Separate outputs into non-numeric and numeric groups
    non_numeric_outputs = [o for o in outputs if not re.search(r'\d+', o)]
    numeric_outputs = [o for o in outputs if re.search(r'\d+', o)]

    # Sort numeric outputs by base name and index, ensuring 'p' comes before 'n'
    numeric_outputs.sort(key=lambda x: (
        re.sub(r'\d+', '', x).replace('p', '0').replace('n', '1'),  # Prioritize 'p' over 'n'
        int(re.search(r'\d+', x).group())
    ))

    # Combine non-numeric outputs first, followed by sorted numeric outputs
    outputs = non_numeric_outputs + numeric_outputs

    # Reverse the order of outputs so that it starts from D_N to D_0
    outputs = outputs[::-1]  # Reverse the output order to D_N to D_0

    return module_name, inputs, outputs

Version_text = """v {xschem version=3.4.5 file_version=1.2
*
* This file is part of XSCHEM,
* a schematic capture and Spice/Vhdl/Verilog netlisting tool for circuit
* simulation.
* Copyright (C) 1998-2023 Stefan Frederik Schippers
*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
}"""
                  


def generate_xschem_symbol(verilog_file, output_sym):
    """Generate an Xschem symbol (.sym) for the given Verilog module with expanded bus signals."""
    module_name, inputs, outputs = parse_verilog(verilog_file)

    # Sort inputs and outputs to ensure bus signals are in descending order
    def sort_bus_signals(signals):
        """Sort bus signals in descending order for proper formatting."""
        numeric_signals = [s for s in signals if re.search(r'\d+', s)]
        non_numeric_signals = [s for s in signals if not re.search(r'\d+', s)]

        # Sort numeric signals by base name and descending index
        numeric_signals.sort(key=lambda x: (
            re.sub(r'\d+', '', x),  # Base name
            -int(re.search(r'\d+', x).group())  # Descending numeric index
        ))

        # Combine non-numeric signals first, followed by sorted numeric signals
        return non_numeric_signals + numeric_signals

    inputs = sort_bus_signals(inputs)
    outputs = sort_bus_signals(outputs)

    # Generate the format string dynamically
    format_inputs = " ".join(f"@@{p}" for p in inputs)
    format_outputs = " ".join(f"@@{p}" for p in outputs)

    symbol = [
        Version_text,
        "G {}",
        "K {type=delay",
        "verilog_ignore=true",
        "vhdl_ignore=true",
        f'format="@name [ {format_inputs} ] [ {format_outputs} ] null @dut',
        '.model @dut @d_cosim_model simulation=@model"',
        "template=\"name=adut",
        "dut=dut",
        "d_cosim_model= d_cosim",
        f"model=./{os.path.basename(verilog_file)[:-2]}.so\" }}",
        "V {}", "S {}", "E {}"
    ]

    pin_distance, width, offset_factor = 20, 100, 30
    total_pins = len(inputs) + len(outputs)
    height_input_side = len(inputs) * pin_distance
    height_output_side = len(outputs) * pin_distance
    total_height = max(height_input_side, height_output_side)
    start_y_input = -height_input_side // 2 + pin_distance // 2
    start_y_output = -height_output_side // 2 + pin_distance // 2

    # Define the structure of lines and boxes as per original .sym. Starting by creating the L lines
    for i, pin_name in enumerate(inputs):
        y = start_y_input + pin_distance * i
        symbol.append(f"L 4 -{width//2 + 2.5 + offset_factor} {y} -{width//2 - 2.5 + offset_factor} {y} {{}}")

    for i, pin_name in enumerate(outputs):
        y = start_y_output + pin_distance * i
        symbol.append(f"L 4 {width//2 + 2.5 + offset_factor} {y} {width//2 - 2.5 + offset_factor} {y} {{}}")
    
    for i, pin_name in enumerate(inputs):
        y = start_y_input + pin_distance * i
        symbol.append(f"B 5 -{width//2 + 2.5 + offset_factor} {y-2.5} -{width//2 - 2.5 + offset_factor} {y+2.5} {{name={pin_name} dir=in verilog_type=wire propag=0}}")

    for i, pin_name in enumerate(outputs):
        y = start_y_output + pin_distance * i
        symbol.append(f"B 5 {width//2 - 2.5 + offset_factor} {y-2.5} {width//2 + 2.5 + offset_factor} {y+2.5} {{name={pin_name} dir=out verilog_type=wire propag=1}}")

    # Module name at the top of the symbol
    symbol.append(f'T {{@name}} 0 {total_height//2 + 5} 0 0 0.12 0.12 {{}}')

    # Module name at the bottom of the symbol
    symbol.append(f'T {{@d_cosim_model}} 0 {-total_height//2 + 5} 0 0 0.12 0.12 {{}}')

    # Printing pin names on the symbol with proper orientation
    for i, pin_name in enumerate(inputs):
        y = start_y_input + pin_distance * i
        symbol.append(f"T {{{pin_name}}} -90 {y-2.5} 0 1 0.12 0.12 {{}}")  # Negative for input side

    for i, pin_name in enumerate(outputs):
        y = start_y_output + pin_distance * i
        symbol.append(f"T {{{pin_name}}} 90 {y-2.5} 0 0 0.12 0.12 {{}}")  # Positive for output side

    # Lines that form the box around the symbol
    symbol.append(f'L 4 {width//2} -{total_height//2} {width//2} {total_height//2} {{}}')
    symbol.append(f'L 4 -{width//2} -{total_height//2} -{width//2} {total_height//2} {{}}')
    symbol.append(f'L 4 -{width//2} {total_height//2} {width//2} {total_height//2} {{}}')
    symbol.append(f'L 4 -{width//2} -{total_height//2} {width//2} -{total_height//2} {{}}')

    with open(output_sym, "w") as f:
        f.write("\n".join(symbol))
    print(f"Xschem symbol written to {output_sym}")

def main():
    """Main function to process Verilog and generate the symbol."""
    if len(sys.argv) != 3:
        print("\nUsage: python generate_sym.py <verilog_file> <symbol_file>")
        print("Example: python generate_sym.py control.v test.sym\n")
        sys.exit(1)


    verilog_file, sym_file = sys.argv[1:3]
    try:
        module_name, inputs, outputs = parse_verilog(verilog_file)
        print(f"Parsed module: {module_name}\nInputs: {inputs}\nOutputs: {outputs}")
        generate_xschem_symbol(verilog_file, sym_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



