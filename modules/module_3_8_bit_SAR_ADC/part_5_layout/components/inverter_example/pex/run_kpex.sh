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

# Cell and schematic names (do NOT include file extensions)
CELL_NAME="inverter"          # The name of your top cell / device under test (DUT)
TESTBENCH_NAME="inverter_tb"  # Name of your testbench schematic (without extension)

# Paths relative to this script or absolute paths
SPICE_DIR="../simulations"    # Directory containing netlist/spice files for testbench
LAYOUT_DIR="../layout"        # Directory containing layout files (.gds etc.)

# Important: Path to your PDK root directory must be set externally in env variable PDK_ROOT

PDK_NAME="ihp_sg13g2"         # Your PDK name (must match PDK_ROOT contents)
MAGICRC="$PDK_ROOT/$PDK/libs.tech/magic/ihp-sg13g2.magicrc"
# The magicrc file for your PDK, used during extraction

# Path to your testbench schematic file (relative or absolute)
# You can override this here if your schematic is located elsewhere
TESTBENCH_PATH="../${TESTBENCH_NAME}.sch"

##############################################################################################################################################################
#                       					⛔ DO NOT TOUCH BELOW THIS LINE ⛔  Unless you see clear issue with your setup :)                 				 #
##############################################################################################################################################################

# Derived paths based on above variables
LAYOUT_GDS="${LAYOUT_DIR}/${CELL_NAME}.gds"
REFERENCE_SPICE="${SPICE_DIR}/${TESTBENCH_NAME}.spice"

# Check if required files exist before proceeding
if [[ ! -f "$PYTHON_ENV" ]]; then
  echo "[ERROR] Python environment activate script not found: $PYTHON_ENV"
  exit 1
fi

if [[ ! -x "$KPEX_MAGIC_EXE" ]]; then
  echo "[ERROR] Magic executable not found or not executable: $KPEX_MAGIC_EXE"
  exit 1
fi

if [[ ! -f "$LAYOUT_GDS" ]]; then
  echo "[ERROR] Layout GDS file not found: $LAYOUT_GDS"
  exit 1
fi

if [[ ! -f "$REFERENCE_SPICE" ]]; then
  echo "[ERROR] Reference spice file not found: $REFERENCE_SPICE"
  exit 1
fi

if [[ ! -f "$TESTBENCH_PATH" ]]; then
  echo "[ERROR] Testbench schematic file not found: $TESTBENCH_PATH"
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
  --gds "$LAYOUT_GDS" \
  --schematic "$REFERENCE_SPICE" \
  --cell "$CELL_NAME" \
  --magicrc "$MAGICRC" \
  --magic_mode RC \
  --magic_cthresh 0.02 \
  --magic_rthresh 50 \
  --magic_short resistor \
  --magic_merge conservative \
  --out_dir ./pex_output

# Create working directory for schematic updates if not exists
mkdir -p xschem

# Find the generated spice file (assuming only one)
spice_location=$(find ./pex_output -type f -name "*.spice" | head -n 1)

if [[ -z "$spice_location" ]]; then
  echo "[ERROR] No .spice file found in pex_output directory"
  exit 1
fi

echo "[INFO] Found extracted spice file: $spice_location"

# Run Python script to fix port ordering in the extracted netlist
echo "[INFO] Reordering subcircuit pins to match original schematic..."
python3 scripts/match_subckt_order.py "$spice_location" "$REFERENCE_SPICE"

# Enter schematic directory
cd xschem || { echo "[ERROR] Failed to enter xschem directory"; exit 1; }

# Run python script to update schematic with PEX subcircuit
echo "[INFO] Updating schematic with PEX subcircuit..."
python3 ../scripts/insert_pex_subckt.py "../$TESTBENCH_PATH" "../$spice_location" # remark this is relatives path native to my setup

# Generate xschemrc file pointing to schematic and symbol folders
# Adjust this path if your schematic/symbols are elsewhere
XSCHEM_PATH="../../"  # relative to current 'xschem' folder (points to symbol for the DUT)

echo "[INFO] Generating xschemrc file..."
python3 ../scripts/xschem_rc.py "$XSCHEM_PATH"

echo "[✅ DONE] Modified schematic generated and saved in: $(pwd)/"
