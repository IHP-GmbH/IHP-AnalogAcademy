#!/bin/bash
set -e  # Exit on error

###############################################################################
#                        ⬇⬇⬇ USER CONFIGURATION ⬇⬇⬇                         #
###############################################################################

# Activate Python environment (edit this if your venv is in another place)
PYTHON_ENV="/home/pedersen/misc/klayout_pex/bin/activate"

# Magic executable for kpex (you can change this if needed)
export KPEX_MAGIC_EXE="$HOME/.local/bin/magic"

# Cell and schematic names (no spaces or extensions needed)
CELL_NAME="inverter"
SYMBOL_NAME="inverter.sym"
SCHEMATIC_NAME="inverter.sch"

# Paths to input files (relative to this script or absolute)
LAYOUT_GDS="../layout/${CELL_NAME}.gds"
REFERENCE_SPICE="../simulations/${CELL_NAME}.spice"

# PDK and magicrc paths
PDK_NAME="ihp_sg13g2"
MAGICRC="$PDK_ROOT/ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc"

###############################################################################
#                       ⛔ DO NOT TOUCH BELOW THIS LINE ⛔                     #
###############################################################################

# Load Python environment
echo "[INFO] Activating Python environment..."
source "$PYTHON_ENV"
echo "[INFO] Using MAGIC executable: $KPEX_MAGIC_EXE"

# Run parasitic extraction
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

# Prepare xschem directory
mkdir -p xschem
cp "../$SYMBOL_NAME" xschem/
cp "../$SCHEMATIC_NAME" xschem/

# Find the PEX spice file
spice_location=$(find ./pex_output -type f -name "*.spice" | head -n 1)

if [[ -z "$spice_location" ]]; then
  echo "[ERROR] No .spice file found in pex_output directory"
  exit 1
fi

echo "[INFO] Found extracted spice file: $spice_location"

# Fix port ordering in the extracted netlist
echo "[INFO] Reordering subcircuit pins to match original schematic..."
python3 scripts/match_subckt_order.py "$spice_location" "$REFERENCE_SPICE"

# Patch the schematic with extracted spice definition
echo "[INFO] Updating schematic with PEX subcircuit..."
python3 scripts/insert_pex_subckt.py "$spice_location"

echo "[✅ DONE] Modified schematic generated and saved to: xschem/"
