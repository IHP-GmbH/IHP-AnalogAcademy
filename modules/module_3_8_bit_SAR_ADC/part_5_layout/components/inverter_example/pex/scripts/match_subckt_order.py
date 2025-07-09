import sys
import re
from pathlib import Path

def get_original_io_order(original_netlist_path):
    io_pins = []

    with open(original_netlist_path, "r") as f:
        for line in f:
            stripped = line.strip()
            # Look for .subckt line (not commented out)
            if stripped.startswith(".subckt"):
                tokens = stripped.split()
                # tokens[0] = '.subckt', tokens[1] = subckt name, rest are pins
                if len(tokens) >= 3:
                    io_pins = tokens[2:]
                    break

    if not io_pins:
        raise ValueError("Could not find IO pins in original schematic")

    return io_pins

def reorder_pex_subckt(pex_path, correct_order):
    with open(pex_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    subckt_found = False

    for line in lines:
        if line.strip().startswith(".subckt") and not subckt_found:
            tokens = line.strip().split()
            subckt_name = tokens[1]
            ports = tokens[2:]

            if set(ports) != set(correct_order):
                raise ValueError("Port names in PEX netlist don't match original IO pins")

            # Create new subckt line with reordered ports
            reordered_line = ".subckt " + subckt_name +"_pex"+" " + " ".join(correct_order) + "\n"
            new_lines.append(reordered_line)
            subckt_found = True
        else:
            new_lines.append(line)

    with open(pex_path, "w") as f:
        f.writelines(new_lines)

    print(f"Rewrote subckt line in {pex_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python patch_pex_order.py <pex_spice_path> <original_schematic_spice_path>")
        sys.exit(1)

    pex_spice = Path(sys.argv[1])
    original_schematic = Path(sys.argv[2])

    io_order = get_original_io_order(original_schematic)
    reorder_pex_subckt(pex_spice, io_order)
