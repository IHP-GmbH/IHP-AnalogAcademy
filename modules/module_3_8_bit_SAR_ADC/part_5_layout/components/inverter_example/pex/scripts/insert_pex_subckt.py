import sys
import os

def load_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def save_text_file(file_path, text):
    with open(file_path, 'w') as f:
        f.write(text)

def read_spice_definition(spice_path):
    with open(spice_path, "r") as f:
        lines = f.readlines()

    subckt_line = next((line for line in lines if line.strip().lower().startswith(".subckt")), None)
    if not subckt_line:
        raise ValueError(f"No .subckt line found in SPICE file: {spice_path}")

    subckt_name = subckt_line.strip().split()[1]

    definition_lines = []
    recording = False
    for line in lines:
        if line.strip().lower().startswith(".subckt"):
            recording = True
        if recording:
            definition_lines.append(line.rstrip())
        if line.strip().lower() == ".ends":
            break

    definition_text = '\n'.join(definition_lines)
    return subckt_name, definition_text

def find_subckt_location(subckt_name, schematic_file):
    text_content = load_text_file(schematic_file)
    search_term = subckt_name + '.sym'
    location = text_content.find(search_term)
    return location

def find_first_curly_brackets_span(text, start_pos):
    open_pos = text.find('{', start_pos)
    if open_pos == -1:
        return None, None

    depth = 1
    for i in range(open_pos + 1, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return open_pos, i
    return None, None

def replace_curly_brackets_content(text, start_idx, end_idx, new_content):
    content = text[start_idx+1:end_idx].strip('\n ')
    lines = content.splitlines()

    name_line_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("name="):
            name_line_index = i
            break

    if name_line_index is None:
        new_lines = ['spice_sym_def="', new_content.strip(), '"'] + lines
    else:
        new_lines = (
            lines[:name_line_index+1] +
            ['spice_sym_def="', new_content.strip(), '"'] +
            lines[name_line_index+1:]
        )

    new_block_content = '\n'.join(new_lines)
    before = text[:start_idx+1]
    after = text[end_idx:]
    return before + '\n' + new_block_content + '\n' + after

def process_pair(spice_path, schematic_path):
    print(f"\nProcessing:\n  SPICE: {spice_path}\n  Schematic: {schematic_path}")
    try:
        subckt_name, definition = read_spice_definition(spice_path)
        print(f"  Subcircuit name: {subckt_name}")
    except Exception as e:
        print(f"  Error reading spice file: {e}")
        return

    location = find_subckt_location(subckt_name, schematic_path)
    if location == -1:
        print(f"  '{subckt_name}.sym' not found in schematic file.")
        return

    schematic_content = load_text_file(schematic_path)
    start_idx, end_idx = find_first_curly_brackets_span(schematic_content, location)
    if start_idx is None:
        print("  No matching curly brackets found after .sym device.")
        return

    new_schematic_content = replace_curly_brackets_content(schematic_content, start_idx, end_idx, definition)

    dir_name, base_name = os.path.split(schematic_path)
    name, ext = os.path.splitext(base_name)
    new_filename = os.path.join(dir_name, f"{name}_modified{ext}")

    save_text_file(new_filename, new_schematic_content)
    print(f"  Replacement done and new schematic file saved as:\n    {new_filename}")



if __name__ == "__main__":
    schematic = "../inverter_tb.sch"
    spice_path = "pex_output/inverter__inverter/magic_RC/inverter.pex.spice"  # replace with actual path

    subckt_name, definition = read_spice_definition(spice_path)

    print(f"Subcircuit name: {subckt_name}")
    print("Definition:")
    print(definition)

    location = find_subckt_location(subckt_name, schematic)
    if location != -1:
        print(f"Found '{subckt_name}.sym' in schematic at position: {location}")

        schematic_content = load_text_file(schematic)
        start_idx, end_idx = find_first_curly_brackets_span(schematic_content, location)
        if start_idx is not None:
            print(f"Replacing curly brackets content from {start_idx} to {end_idx}...")
            new_schematic_content = replace_curly_brackets_content(schematic_content, start_idx, end_idx, definition)

            # Prepare new filename with _pex suffix before extension
            dir_name, base_name = os.path.split(schematic)
            name, ext = os.path.splitext(base_name)
            new_filename = f"{name}_pex{ext}"

            # Ensure xschem/ exists and define full path there
            xschem_dir = os.path.join(os.getcwd(), "xschem")
            os.makedirs(xschem_dir, exist_ok=True)
            xschem_path = os.path.join(xschem_dir, new_filename)

            # Save to xschem/ folder
            save_text_file(xschem_path, new_schematic_content)
            print(f"Replacement done. New schematic saved to:\n  {xschem_path}")
        else:
            print("No curly brackets block found after .sym line.")
    else:
        print(f"'{subckt_name}.sym' not found in schematic.")
