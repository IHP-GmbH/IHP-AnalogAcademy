import sys
from pathlib import Path

def get_original_io_order(original_netlist_path):
    io_pins = []

    with open(original_netlist_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("*"):
                continue
            if stripped.lower().startswith(".subckt"):
                tokens = stripped.split()
                if len(tokens) >= 3:
                    print(f"[INFO] Found .subckt in original: {stripped}")
                    io_pins = tokens[2:]
                    break

    if not io_pins:
        raise ValueError(f"Could not find IO pins in original schematic: {original_netlist_path}")

    return io_pins

def reorder_pex_subckt(pex_path, correct_order):
    with open(pex_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    subckt_found = False

    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith(".subckt") and not subckt_found:
            tokens = stripped.split()
            subckt_name = tokens[1]
            ports = tokens[2:]

            # Case-insensitive set comparison
            ports_lower = [p.lower() for p in ports]
            correct_lower = [p.lower() for p in correct_order]

            if set(ports_lower) != set(correct_lower):
                print("[ERROR] Port name mismatch!")
                print("[DEBUG] PEX ports     :", ports)
                print("[DEBUG] Schematic IOs:", correct_order)
                raise ValueError("Port names in PEX netlist don't match original IO pins")

            # Map from lower-case pin name to original-cased PEX name
            port_map = {p.lower(): p for p in ports}

            reordered_ports = [port_map[p.lower()] for p in correct_order]
            reordered_line = f".subckt {subckt_name}_pex {' '.join(reordered_ports)}\n"
            new_lines.append(reordered_line)
            subckt_found = True
        else:
            new_lines.append(line)

    with open(pex_path, "w") as f:
        f.writelines(new_lines)

    print(f"[INFO] Rewrote subckt line in {pex_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python match_subckt_order.py <pex_spice_path> <original_schematic_spice_path>")
        sys.exit(1)

    pex_spice = Path(sys.argv[1])
    original_schematic = Path(sys.argv[2])

    print(f"[INFO] Found extracted spice file: {pex_spice}")
    print(f"[INFO] Reordering subcircuit pins to match original schematic...")

    io_order = get_original_io_order(original_schematic)
    reorder_pex_subckt(pex_spice, io_order)
