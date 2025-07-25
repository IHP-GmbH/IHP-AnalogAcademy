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

    subckt_line_index = next((i for i, line in enumerate(lines) if line.strip().lower().startswith(".subckt")), None)
    if subckt_line_index is None:
        raise ValueError(f"No .subckt line found in SPICE file: {spice_path}")

    parts = lines[subckt_line_index].strip().split()
    subckt_name = parts[1]
    new_subckt_name = subckt_name
    parts[1] = new_subckt_name
    lines[subckt_line_index] = ' '.join(parts) + '\n'

    definition_lines = []
    recording = False
    for line in lines:
        if line.strip().lower().startswith(".subckt"):
            recording = True
        if recording:
            definition_lines.append(line.rstrip())
        if line.strip().lower() == ".ends":
            break

    return new_subckt_name, '\n'.join(definition_lines)

def find_subckt_location(subckt_name, schematic_file):
    text_content = load_text_file(schematic_file)
    return text_content.find(subckt_name + '.sym')

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

def replace_curly_brackets_content(text, start_idx, end_idx, new_content, subckt_name):
    content = text[start_idx+1:end_idx].strip('\n ')
    lines = content.splitlines()

    name_line_index = next((i for i, line in enumerate(lines) if line.strip().startswith("name=")), None)
    schematic_line = "schematic=" + subckt_name
    if name_line_index is None:
        new_lines = ['spice_sym_def="', new_content.strip(), '"'] + lines
    else:
        new_lines = (
            lines[:name_line_index+1] +
            [schematic_line] +
            ['spice_sym_def="', new_content.strip(), '"'] +
            lines[name_line_index+1:]
        )

    return text[:start_idx+1] + '\n' + '\n'.join(new_lines) + '\n' + text[end_idx:]

def process_pair(spice_path, schematic_path):
    print(f"\nProcessing:\n  SPICE: {spice_path}\n  Schematic: {schematic_path}")
    try:
        subckt_name, definition = read_spice_definition(spice_path)
        print(f"  Subcircuit name: {subckt_name}")
    except Exception as e:
        print(f"  Error reading spice file: {e}")
        return

    # If subckt_name ends with '_pex', strip it for schematic search
    search_subckt_name = subckt_name
    if subckt_name.endswith("_pex"):
        search_subckt_name = subckt_name[:-4]

    location = find_subckt_location(search_subckt_name, schematic_path)
    if location == -1:
        print(f"  '{search_subckt_name}.sym' not found in schematic file.")
        return

    schematic_content = load_text_file(schematic_path)
    start_idx, end_idx = find_first_curly_brackets_span(schematic_content, location)
    if start_idx is None:
        print("  No matching curly brackets found after .sym device.")
        return

    new_schematic_content = replace_curly_brackets_content(
        schematic_content, start_idx, end_idx, definition, subckt_name
    )

    # Save the file in the current working directory (where script is run)
    base_name = os.path.basename(schematic_path)
    name, ext = os.path.splitext(base_name)
    new_filename = os.path.join(os.getcwd(), f"{name}_pex{ext}")

    save_text_file(new_filename, new_schematic_content)
    
    print(f"  Replacement done and new schematic file saved as:\n    {new_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:\n  python3 script.py <schematic.sch> <spice_file.spice>")
        sys.exit(1)

    schematic = sys.argv[1]
    spice_path = sys.argv[2]

    print(f"Starting processing with schematic='{schematic}', spice='{spice_path}'")  # Debug print

    process_pair(spice_path, schematic)
