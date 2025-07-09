#!/bin/bash
source /home/pedersen/misc/klayout_pex/bin/activate

export KPEX_MAGIC_EXE="$HOME/.local/bin/magic" 
echo "KPEX_MAGIC_EXE is: $KPEX_MAGIC_EXE"

kpex \
  --pdk ihp_sg13g2 \
  --magic \
  --gds input_pair_cm.gds \
  --schematic schematic_mod/simulations/input_pair_cm.spice \
  --cell input_pair_cm \
  --magicrc /home/pedersen/IHP-Open-PDK/ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc\
  --magic_mode RC \
  --magic_cthresh 0.02 \
  --magic_rthresh 50 \
  --magic_short resistor \
  --magic_merge conservative \
  --out_dir ./pex_output
