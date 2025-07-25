#!/bin/bash
set -e

###############################################################################
#                        ⬇⬇⬇ USER CONFIGURATION ⬇⬇⬇                         #
###############################################################################

# Activate Python environment (adjust this path to your Python venv activate script) Or if you python version is >3.12 ignore asuming klayout_pex is installed
PYTHON_ENV="$HOME/misc/klayout_pex/bin/activate" 
# Example: /home/username/misc/klayout_pex/bin/activate

# Path to Magic executable used by kpex (adjust if installed elsewhere)
KPEX_MAGIC_EXE="$HOME/.local/bin/magic" 
# Example: /usr/local/bin/magic or ~/.local/bin/magic

#Path to symbol
SYM_DIR="./DIFF_COMPARATOR.sym"       # Asuming you have a symbol for the DUT

LAYOUT_DIR="../layout/DIFF_COMPARATOR.gds"        # Path to the GDS file

# Important: Path to your PDK root directory must be set externally in env variable PDK_ROOT, otherwise give absolute path
PDK_NAME="ihp_sg13g2"         # Your PDK name (must match PDK_ROOT contents)
MAGICRC="$PDK_ROOT/$PDK/libs.tech/magic/ihp-sg13g2.magicrc" # The magicrc file for your PDK, used during extraction

SCHEMATIC="../layout/lvs_netlist/DIFF_COMPARATOR.spice" # Spicefile of the comparator from Schematic or LVS (Used for pex to perform LVS and script to organize IO)

##############################################################################################################################################################
#                       					⛔ DO NOT TOUCH BELOW THIS LINE ⛔  Unless you see clear issue with your setup :)                 				 #
##############################################################################################################################################################


# Check if required files exist before proceeding
if [[ ! -f "$PYTHON_ENV" ]]; then
  echo "[ERROR] Python environment activate script not found: $PYTHON_ENV"
  exit 1
fi

if [[ ! -x "$KPEX_MAGIC_EXE" ]]; then
  echo "[ERROR] Magic executable not found or not executable: $KPEX_MAGIC_EXE"
  exit 1
fi

if [[ ! -f "$LAYOUT_DIR" ]]; then
  echo "[ERROR] Layout GDS file not found: $LAYOUT_DIR"
  exit 1
fi


if [[ ! -f "$MAGICRC" ]]; then
  echo "[ERROR] Magicrc file for PDK not found: $MAGICRC"
  exit 1
fi

# Activate Python virtual environment
echo "[INFO] Activating Python environment..."
source "$PYTHON_ENV"

echo "[INFO] Using MAGIC executable: $KPEX_MAGIC_EXE"

# Run parasitic extraction with kpex
echo "[INFO] Running parasitic extraction with KPEX..."
kpex \
  --pdk "$PDK_NAME" \
  --magic \
  --schematic "$SCHEMATIC"\
  --gds "$LAYOUT_DIR" \
  --magicrc "$MAGICRC" \
  --magic_mode RC \
  --magic_cthresh 0.02 \
  --magic_rthresh 50 \
  --magic_short resistor \
  --magic_merge conservative \
  --out_dir ./pex_output

# Find the generated spice file (assuming only one)
spice_location=$(find ./pex_output -type f -name "*.spice" ! -name "*_dummy_schematic.spice" | head -n 1)


if [[ -z "$spice_location" ]]; then
  echo "[ERROR] No .spice file found in pex_output directory"
  exit 1
fi

echo "[INFO] Found extracted spice file: $spice_location"

# Run Python script to fix port ordering in the extracted netlist
echo "[INFO] Reordering subcircuit pins to match original schematic..."
echo "$spice_location"
echo "$SCHEMATIC"

python3 python/match_subckt_order.py "$spice_location" "$SCHEMATIC"



echo "[INFO] Creating DUT symbol with pex netlist"
python3 python/insert_netlist_to_sym.py "$spice_location" "$SYM_DIR" xschem_pex_symbol

cd xschem_pex_symbol
echo "[✅ DONE] Modified symbol, including pex netlist generated and saved in: $(pwd)/"
