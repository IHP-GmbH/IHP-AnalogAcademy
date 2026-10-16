# Part 3 – Matched Layout and Physical Verification

[Previous: Simulations](../part_2_simulations/README.md) · [Module overview](../README.md) · [Next: PEX and Finishing](../part_4_pex_and_finishing/README.md)

The comparator's layout is part of its offset and timing design. Build the layout around matched device groups, balanced regenerative nodes, and a compact clock route.

## Open the Reference Layout

With KLayout's SG13G2 technology and PCells installed and the [module environment](../README.md#get-the-design-and-set-up-paths) configured:

```bash
klayout -e "$CMP7345_ROOT/layout/klayout/CMP7345.gds"
```

![Final comparator layout](../.media/layout-final.png)

For the one-day format, inspect and verify this implementation. For the two-day format, reconstruct the matched sub-blocks in your exercise layout and compare them with the supplied GDS views.

## Build the Matched Sub-Blocks

| Block | Reference GDS under `layout/klayout/` | Main objective |
|-------|--------------------------------------|----------------|
| Input differential pair | `diff_pair/diff_pair.gds` | Matching, common-centroid placement, and a uniform local environment |
| NMOS cross-coupled pair | `cc_nmos_pair/cc_pair_nmos.gds` | Balanced discharge paths and node capacitances |
| PMOS cross-coupled pair | `cc_pmos_pair/cc_pair_pmos.gds` | Symmetric regeneration and supply connections |

![Common-centroid differential-pair layout](../.media/layout_diff_pair.png)

1. Start from the final schematic's unit devices and identify the active fingers and dummies.
2. Preserve orientation, local surroundings, and matching symmetry within each pair.
3. Add local `ptap1`/`ntap1` connections and the protection structures represented in the schematic.
4. Assemble the input and cross-coupled pairs, then add the tail and reset devices.
5. Route within **Metal1–Metal3**, balancing both branches' wire lengths, vias, and loading.
6. Keep the clock route short and inspect coupling to sensitive input and regenerative nodes.
7. Check that labels, supply connections, and sub-block interfaces agree with the final schematic.

Common-centroid placement helps mitigate spatial gradients; random mismatch still requires sufficient device area and statistical analysis. Symmetric placement also needs symmetric routing to produce balanced parasitics.

## Design Rule Checking (DRC)

DRC checks the physical geometry against process requirements. Run it during layout construction so enclosure, spacing, contact, and routing errors are corrected early.

From the layout directory, the workshop flow can be expressed using the installed PDK verification script:

```bash
cd "$CMP7345_ROOT/layout/klayout"
python3 "$PDKPATH/libs.tech/klayout/tech/drc/run_drc.py" \
  --path=CMP7345.gds \
  --run_mode=deep \
  --run_dir=drc_cmp7345 \
  --no_density
```

This invocation disables density checks for early cell-level debugging. Use the [verification documentation](https://ihp-open-pdk-docs.readthedocs.io/en/latest/verification.html) and the installed script's `--help` for revision-specific options. Load the generated `.lyrdb` marker database in KLayout and inspect the highlighted geometry. Full density checking is part of the finishing exercise in Part 4.

## Layout Versus Schematic (LVS)

LVS checks whether the layout implements the intended circuit. Use the **final layout-compatible schematic**, including its hierarchy, dummies, taps, and protection devices, as the reference.

Inspect or regenerate `netlist/schematic/CMP7345-final.spice` before running LVS. The stored export has its top-level `.subckt` and `.ends` lines commented out. In your exercise copy, replace the top-level `**.subckt` line with:

```spice
.subckt CMP7345 v- v+ vss vdd clk vout2 vout1
```

Replace the corresponding `**.ends` line, immediately before the child subcircuit definitions, with `.ends CMP7345`. This gives the reference the same top-level name as the layout's `CMP7345` cell. Keep the devices, ports, and child subcircuit definitions intact. If you regenerate the reference from Xschem instead, configure its subcircuit export to provide the same interface.

After preparing that reference, run:

```bash
cd "$CMP7345_ROOT/layout/klayout"
python3 "$PDKPATH/libs.tech/klayout/tech/lvs/run_lvs.py" \
  --layout=CMP7345.gds \
  --netlist="$CMP7345_ROOT/netlist/schematic/CMP7345-final.spice" \
  --run_dir=lvs_cmp7345 \
  --run_mode=flat
```

Inspect the execution log and the generated `.lvsdb` in KLayout's netlist browser. Follow mismatches back to the relevant devices and nets. Typical comparator debugging questions are:

- Are `vout1` and `vout2` connected to the intended cross-coupled branches?
- Do parallel unit devices add up to the intended effective width?
- Are well/substrate ties and protection structures recognized correctly?
- Do all top-level inputs, supplies, and clock connections match?

Establish connectivity with LVS before interpreting a PEX simulation. A plausible waveform by itself does not establish that the layout implements the intended schematic.

### Exercise Outcome

Produce a matching-aware layout and keep the DRC/LVS reports with a record of any outstanding issues. Be able to explain the device placement, the purpose of the dummies and taps, and how layout asymmetry can become an electrical error.
