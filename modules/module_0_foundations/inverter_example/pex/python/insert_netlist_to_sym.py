import sys
import os

def extract_netlist_and_topcell(spice_path):
    with open(spice_path, 'r') as f:
        lines = f.readlines()

    netlist = []
    topcell = None
    inside_subckt = False

    for line in lines:
        if line.strip().startswith(".subckt"):
            parts = line.strip().split()
            if len(parts) > 1:
                topcell = parts[1]
            inside_subckt = True
        if inside_subckt:
            netlist.append(line.rstrip())
        if line.strip().startswith(".ends"):
            break

    if not topcell:
        raise ValueError("Topcell name not found in SPICE file.")

    return topcell, "\n".join(netlist)

def modify_sym_file(sym_path, output_dir, topcell, netlist):
    with open(sym_path, 'r') as f:
        sym_lines = f.readlines()

    new_sym_lines = []
    inserted = False

    for line in sym_lines:
        if line.strip().startswith("K {type=subcircuit"):
            new_sym_lines.append(line)
            continue
        elif line.strip().startswith("template=") and not inserted:
            new_template = (
                f'template="name=x1\n'
                f'schematic={topcell}\n'
                f'spice_sym_def=\n'
                f'\\\\"\n'
                f'{netlist}\n'
                f'\\\\"\n'
                f'"'
            )
            new_sym_lines.append(new_template + "\n")
            inserted = True
        else:
            new_sym_lines.append(line)

    filename = os.path.basename(sym_path)
    out_path = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(out_path, 'w') as f:
        f.writelines(new_sym_lines)

    print(f"Saved modified .sym to: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python insert_netlist_to_sym.py <netlist.spice> <symbol.sym> <output_folder>")
        sys.exit(1)

    spice_file = sys.argv[1]
    sym_file = sys.argv[2]
    output_folder = sys.argv[3]

    topcell, netlist = extract_netlist_and_topcell(spice_file)
    modify_sym_file(sym_file, output_folder, topcell, netlist)
