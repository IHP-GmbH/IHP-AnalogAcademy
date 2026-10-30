# Part 6 – Chip Finishing and Design Improvements

[Previous: Parasitic Extraction](../part_5_pex/README.md) · [Module overview](../README.md)

The comparator is a reusable core cell. Integrating it into a chip adds a physical context: surrounding circuitry, power distribution, I/O, a chip boundary, and process-required finishing structures. This part explains how fill and density affect that context, then uses the simulation results to identify the next design iteration.

## Why Dummy Fill Matters

Sparse and dense material regions behave differently during chemical-mechanical polishing. Dummy fill improves local density uniformity and helps maintain planarity across subsequent process layers. It is not intended to perform a circuit function, but it is physically present and can change coupling capacitance around sensitive nets.

For this comparator, that creates two related tasks:

- Meet the density and geometric requirements in the intended chip-level region.
- Reconsider the parasitic environment of the inputs, clock, and regenerative nodes after fill is inserted.

Cell-level DRC with density disabled is useful during construction. It does not establish chip-level density compliance.

## Sealring and Top-Level Context

The final chip-level layout requires the process-provided sealring. Place it around the intended die boundary using the SG13G2 library and the applicable integration rules. A sealring belongs to the chip boundary, rather than around every comparator instance.

Prepare a separate top-level exercise layout containing the comparator and its intended surroundings. Keep the verified cell hierarchy and port names so that subsequent verification can still identify the circuit. For a complete chip, plan I/O, power, and protection structures using the target process documentation.

## Generate Fill in KLayout

The SG13G2 menus expose the following operations:

| Operation | Purpose |
|-----------|---------|
| **Fill Activ/GatPoly** | Insert front-end filler according to the process rules. |
| **Fill Metal** | Insert filler on the applicable metal layers. |
| **Fill Top Metal** | Handle the process's top-metal fill requirements. |
| **Density Report** | Inspect the resulting density distribution. |

Use the [PDK filler documentation](https://ihp-open-pdk-docs.readthedocs.io/en/latest/finishing/filler.html) for layer selection, exclusion regions, and fill settings. The comparator's Metal1–Metal3 routing restriction is a core-design choice; finishing must follow the requirements of the complete target process.

### Scripted Fill

After saving the prepared chip-level layout as `design_nofill.gds`, run this command from its working directory using the [module PDK environment](../README.md#get-the-design-and-set-up-paths):

```bash
klayout -n sg13g2 -zz -r \
  "$PDKPATH/libs.tech/klayout/tech/scripts/filler.py" \
  -rd output_file=./design_filled.gds \
  design_nofill.gds
```

The technology is selected with `-n sg13g2`; `-r` runs the fill script, and `output_file` keeps the filled result separate from the input. Inspect the output GDS and run log before continuing.

Fill density can be adjusted through the supported pattern dimensions and spacing. For Metals 1–5, the documented minimum spacing between fillers is 0.42 µm; use the rule values and conditions from the installed PDK when selecting a pattern. Increasing density must still preserve spacing and enclosure rules.

### Density and Final Verification

1. Open the filled top-level layout and run **Density Report**.
2. Locate low- or high-density regions and inspect the layers and analysis windows involved.
3. Adjust fill using the PDK's permitted settings and rerun the report.
4. Run the full DRC rule set with density checks enabled.
5. Reconfirm the circuit connectivity and regenerate PEX when the physical changes affect the extracted view.

For example, from the directory containing the filled layout:

```bash
python3 "$PDKPATH/libs.tech/klayout/tech/drc/run_drc.py" \
  --path=design_filled.gds \
  --run_mode=deep \
  --run_dir=drc_filled
```

Unlike the early cell-level example, this command does not pass `--no_density`. For larger layouts, a density-only run can shorten debugging, followed by a complete run for the final result. Inspect boundary-related markers in the context of the analysis region and the documented rule conditions.

The PDK also describes a `gdsfill` flow with density analysis and automated fill generation. When using that flow, keep its configuration and outputs with the design so the final physical result can be reproduced.

## Process Portability

SG13G2 provides a SiGe BiCMOS device set and a seven-layer metal stack, including five thin and two thick top metals. SG13CMOS removes the bipolar option; SG13CMOS5L uses a reduced device set and metal stack suitable for education-oriented designs.

The comparator's low-voltage MOS core and Metal1–Metal3 routing make it a useful portability exercise. A reduced process may not provide isolated NMOS devices or MIM capacitors, so auxiliary circuitry must also respect the selected device set. Re-run model-based simulation, PCell generation, physical verification, and extraction with the intended process. A shared topology alone does not establish cross-process equivalence.

## PVT Characterization

Extend the verified testbench across **process, voltage, and temperature** conditions. Define a matrix before running it:

| Axis | Conditions to select |
|------|----------------------|
| Process | Typical and supported slow/fast/mixed MOS corners; appropriate passive corners |
| Supply | Nominal 1.2 V and the minimum/maximum values permitted by the design specification and device limits |
| Temperature | Nominal and the intended operating-range endpoints |
| Input | Both polarities, near-threshold differences, and selected common-mode levels |
| Loading | Intended output loads and representative input-source impedance |

For every condition, use the same definitions of valid logic level, decision time, and reset completeness. Record failed or unresolved comparisons along with successful delay values. Check both maximum delay and input disturbance; the corner with the fastest nominal regeneration need not be the best for kickback.

A characterization tool such as CACE can automate the matrix once the individual benches and measurements work. Automate the conditions, simulator invocation, result extraction, and pass/fail classification together. Retain the tool/PDK revisions and statistical seeds where applicable.

## Improve the Comparator Using Measured Results

### Input-Pair Area and Offset

The final input pair uses eight 1 µm by 0.26 µm active units per side. Compare this baseline with a larger-area option while tracking three quantities together: offset distribution, delay, and input kickback. Report the mean offset and the spread; a $3\sigma$ value describes the distribution width and is not a hard worst-case bound.

Increasing area reduces the first-order random threshold mismatch estimate, but it also adds capacitance. If offset remains too large for the application, evaluate whether gain before the latch is more effective than further increasing the latch's input devices.

### Early Gain and Tail Strength

The input pair develops useful gain before strong regeneration begins. A qualitative design guide is the input-pair $g_m/I_{tail}$ ratio and the length of time the pair remains in a useful operating region. A stronger tail can accelerate discharge while reducing the early amplification interval and increasing switching disturbance.

Sweep tail width and inspect `P/Q` separation before the outputs diverge. Measure delay, offset, and kickback for each setting. This exposes the architectural coupling between sensing gain and regeneration speed: the classical StrongARM structure uses the same current path for both.

### Reset Equalization and Dynamic Offset

Unequal reset action can leave a residual differential voltage even when the two branches appear geometrically symmetric. Compare `P-Q` immediately before evaluation after alternating positive and negative decisions.

As an extension, add a clock-controlled equalization switch between the input-pair drain nodes during reset. Check whether it reduces history-dependent offset, and account for its additional capacitance and charge injection. Repeat the experiment with mismatch in the reset devices so the improvement is evaluated under the condition it is intended to address.

### Kickback and Common-Mode Sensitivity

Keep the input routes short and balanced and use representative impedances on both sides. Compare kickback around the tail-release boundary, then sweep common mode to observe the available headroom and early gain. A preamplifier can reduce the latch's input-referred error and isolate the source, at the cost of additional power, area, noise, and delay.

For requirements that push both speed and input-referred accuracy, comparing a preamplified or double-tail comparator with the StrongARM baseline is a useful further exercise. Use the same source, load, timing budget, and measurement definitions for a meaningful comparison.

## Final Design Record

Collect the following results from all six parts:

- Schematic view, transistor dimensions, symbol interface, and design/PDK revisions.
- Nominal waveforms and automatic timing measurements for both input polarities.
- Mismatch/process distributions, sample counts, and unresolved-case classification.
- Common-mode and kickback observations under representative source loading.
- Matched layout hierarchy, DRC/LVS reports, and any issues requiring further work.
- Extracted netlist, extraction options, and pre-/post-layout comparison.
- Chip-level fill/density results and the selected PVT characterization conditions.

### Exercise Outcome

Explain the dominant limitation of the current implementation and propose one measured design improvement. A complete result connects the circuit choices, statistical behavior, layout, and extracted performance rather than treating each step as an isolated drawing or simulation.
