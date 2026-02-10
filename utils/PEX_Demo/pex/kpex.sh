#!/bin/bash
set -e

# Hardcoded paths (except PDK stuff)

LAYOUT_PATH="../layout/inverter.gds"
SCHEMATIC="../simulations/inverter.spice"


PDK_NAME="ihp_sg13g2"
MAGICRC="$PDK_ROOT/$PDK/libs.tech/magic/ihp-sg13g2.magicrc" # The magicrc file for your PDK, used during extraction


# Run parasitic extraction with kpex
kpex \
  --pdk "$PDK_NAME" \
  --magic \
  --schematic "$SCHEMATIC" \
  --gds "$LAYOUT_PATH" \
  --magicrc "$MAGICRC" \
  --magic_mode RC \
  --magic_cthresh 0.02 \
  --magic_rthresh 50 \
  --magic_short resistor \
  --magic_merge conservative \
  --out_dir ./pex_output

