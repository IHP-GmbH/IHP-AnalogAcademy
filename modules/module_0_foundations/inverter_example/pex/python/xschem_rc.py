import sys
def generate_xschemrc(custom_paths):
    lines = [
        "# xschemrc - Custom configuration file for xschem",
        "# This file sources another xschemrc file from a known location",
        "",
        "# Source the base configuration from a known location",
        "source $::env(PDK_ROOT)/$::env(PDK)/libs.tech/xschem/xschemrc",
        "",
        "# (Optional) Add any custom overrides or extensions below",
        '# set xschem_library_path /home/user/my_libs',
        '# set xschem_gui_font "Monospace 10"',
        "",
        "append XSCHEM_LIBRARY_PATH :$PDK_ROOT/ihp-sg13g2/libs.tech/xschem"
    ]

    # Append each custom path with the prefix "../"
    for path in custom_paths:
        lines.append(f"append XSCHEM_LIBRARY_PATH :{path}")

    return "\n".join(lines) + "\n"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 make_xschemrc.py <path1> [<path2> ... <pathN>]")
        sys.exit(1)

    custom_paths = sys.argv[1:]
    content = generate_xschemrc(custom_paths)

    with open("xschemrc", "w") as f:
        f.write(content)

    print(f"xschemrc file generated with {len(custom_paths)} custom paths.")

if __name__ == "__main__":
    main()
