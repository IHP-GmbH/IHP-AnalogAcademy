# Part 4 – Physical Verification

[Previous: Layout](../part_3_layout/README.md) · [Module overview](../README.md) · [Next: Parasitic Extraction](../part_5_pex/README.md)

Physical verification asks two different questions. **Design rule checking (DRC)** checks layout geometry against the process rules. **Layout versus schematic (LVS)** checks whether the recognized devices and connections implement the intended circuit. Both are needed before attributing post-layout behavior to parasitics.

Use the [module environment](../README.md#get-the-design-and-set-up-paths) and the SG13G2 verification decks installed with the PDK.

## Design Rule Checking

The rule sets cover different levels of checking:

| Rule group | Purpose |
|------------|---------|
| Precheck/minimal rules | Early structural and layer-usage checks |
| Main rules | Device and interconnect geometry, including density by default |
| Extra rules | Additional specialized or more expensive checks |

During layout construction, fix width, spacing, enclosure, contact, and via errors as soon as they appear. At the comparator level, pay particular attention to the matched input devices, local taps, clock-route jogs, and output interconnect.

### Command-Line DRC

```bash
cd "$CMP7345_ROOT/layout/klayout"
python3 "$PDKPATH/libs.tech/klayout/tech/drc/run_drc.py" \
  --path=CMP7345.gds \
  --run_mode=deep \
  --run_dir=drc_cmp7345 \
  --no_density
```

The input is the comparator GDS; `deep` selects hierarchical processing and `run_dir` keeps the results together. `--no_density` is useful for an early cell-level iteration. Density is checked later in the intended chip context, as described in Part 6.

Useful options include `--topcell` for an explicit top cell, `--table` for a selected rule table, and `--antenna` for antenna checks. Consult the installed script's `--help` and [PDK verification documentation](https://ihp-open-pdk-docs.readthedocs.io/en/latest/verification.html) for supported options.

### Read and Debug the Results

The output directory contains a run log, the executed rule deck, and a marker database such as `CMP7345.lyrdb`. Open the generated database with the layout:

```bash
klayout "$CMP7345_ROOT/layout/klayout/CMP7345.gds" \
  -m "$CMP7345_ROOT/layout/klayout/drc_cmp7345/CMP7345.lyrdb"
```

Use the actual output filename reported by the run if it differs. For each marker:

1. Read the rule description and locate the failing shapes.
2. Check the relevant layers and dimensions, including enclosure around contacts/vias.
3. Correct the geometry while preserving matching. If an edit changes one branch's routing, review the corresponding branch too.
4. Run the affected checks again, then run the broader rule set before proceeding.

An empty-looking layout view is not a result: confirm that the run completed and that the correct marker database and top cell were loaded.

## Prepare the LVS Reference

Use the **final layout-compatible schematic**, including its hierarchy, dummies, taps, and protection devices. The basic architectural view does not describe all of these physical structures.

Inspect or regenerate `netlist/schematic/CMP7345-final.spice`. The stored export has its top-level `.subckt` and `.ends` lines commented out. In your exercise copy, replace the top-level `**.subckt` line with:

```spice
.subckt CMP7345 v- v+ vss vdd clk vout2 vout1
```

Replace the corresponding `**.ends` line immediately before the child subcircuit definitions with:

```spice
.ends CMP7345
```

This gives the schematic reference the same top-level name as the layout's `CMP7345` cell. Keep the transistor instances and child definitions intact. If exporting directly from Xschem, configure the subcircuit export to provide the same interface. Compare device widths, multiplicities, and body networks before starting the run.

## Layout Versus Schematic

```bash
cd "$CMP7345_ROOT/layout/klayout"
python3 "$PDKPATH/libs.tech/klayout/tech/lvs/run_lvs.py" \
  --layout=CMP7345.gds \
  --netlist="$CMP7345_ROOT/netlist/schematic/CMP7345-final.spice" \
  --run_dir=lvs_cmp7345 \
  --run_mode=flat
```

The LVS deck recognizes devices from the process layers, extracts connections, and compares them with the schematic reference. Simplification can combine equivalent parallel devices or remove unused structures; interpret that reduction when comparing device counts.

For debugging, `--no_simplify` exposes more of the original extracted topology. `--no_series_res` and `--no_parallel_res` help when resistor reduction obscures a connection; `--verbose` provides additional logging. Check which switches your installed deck supports.

### Inspect the Netlist Browser

The run produces an execution log, extracted circuit data, and an LVS database. Load the generated database in KLayout:

```bash
klayout "$CMP7345_ROOT/layout/klayout/CMP7345.gds" \
  -mn "$CMP7345_ROOT/layout/klayout/lvs_cmp7345/CMP7345.lvsdb"
```

Follow each mismatch from the circuit browser back to the shapes. Typical comparator issues are:

| Mismatch | Investigation |
|----------|---------------|
| Swapped outputs | Trace each output through both cross-coupled pairs. |
| Missing/wrong body connection | Inspect well/substrate layers, taps, and hierarchy ports. |
| Device-count or width mismatch | Sum active parallel fingers and separate dummies from signal devices. |
| Unexpected source/drain mapping | Check extracted connectivity and the device model's treatment of terminal interchange. |
| Unmatched top-level ports | Compare top-cell names, pin labels, and the reference subcircuit interface. |
| Unrecognized protection element | Check the layer combination and device definition against the PDK. |

Compare both effective device area and connectivity. Equal transistor counts alone do not prove the two cross-coupled branches are wired correctly.

## GUI-Based Verification

To expose the SG13G2 verification menus, start KLayout with the PDK search paths:

```bash
KLAYOUT_PATH="$PDKPATH/libs.tech/klayout:$PDKPATH/libs.tech/klayout/tech:" \
  klayout -e "$CMP7345_ROOT/layout/klayout/CMP7345.gds"
```

Select the top cell and configure DRC options from the SG13G2 menus. For LVS, explicitly select the reference netlist. The GUI may otherwise search near the layout for a matching `.cdl`, `.spice`, or `.cir` file, which can select a stale export if several versions are present.

The GUI is convenient for inspecting individual errors; the command-line flow provides a reproducible record of inputs, options, and outputs. Both should use the same intended cell and PDK revision.

## Verification Sequence

1. Run DRC while building the matched blocks.
2. Correct the assembled cell's geometry errors.
3. Run LVS against the final schematic and resolve device, port, and connectivity mismatches.
4. Retain the GDS, reference netlist, PDK revision, logs, and result databases together.
5. Use that verified layout for the extraction exercise in Part 5.

PEX does not replace LVS. An incorrectly connected extracted circuit can still produce plausible transients, so establish the circuit correspondence before interpreting differences in delay or kickback.

### Exercise Outcome

Keep a DRC/LVS result set and a short explanation of the corrections made. Distinguish geometry errors from electrical mismatches, and identify any checks deferred to the chip-level finishing stage.
