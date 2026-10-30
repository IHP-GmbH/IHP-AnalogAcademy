# Part 5 – Parasitic Extraction and Post-Layout Simulation

[Previous: Physical Verification](../part_4_physical_verification/README.md) · [Module overview](../README.md) · [Next: Chip Finishing](../part_6_chip_finishing/README.md)

Parasitic extraction (PEX) adds the interconnect loading that is missing from the ideal schematic. In a dynamic latch, this can change regeneration delay, reset balance, input disturbance, and the minimum input difference that resolves within the available time.

The extracted view describes the devices and connections recognized in layout, together with the parasitic elements produced by the selected extraction method. Device fingers can appear as separate instances, and internal node names can differ from the schematic hierarchy. Interpret these changes electrically rather than expecting textually identical netlists.

| Parasitic location | Possible effect |
|-------------------|-----------------|
| Regenerative nodes | Longer decision time and a changed regeneration time constant |
| Unequal branch loading | Systematic decision preference and unequal reset recovery |
| Input-to-input or clock-to-input coupling | Changed differential/common-mode kickback |
| Output-to-supply or output-to-output coupling | Changed output transitions and buffer loading |

The same layout can therefore remain logically correct while its useful timing margin changes.

## Extract the Comparator

After the DRC/LVS work in Part 4, run Magic-based extraction through KLayout-PEX. Use the [module environment](../README.md#get-the-design-and-set-up-paths):

```bash
cd "$CMP7345_ROOT/layout/klayout"
kpex --pdk ihp-sg13g2 --magic --magic_cthresh=2.0 --gds CMP7345.gds
```

Inspect the extraction log for the generated SPICE file and output directory. Compare it with the supplied `netlist/pex/CMP7345.pex.spice`. Record the extraction options, especially the capacitance threshold, when comparing results.

The options select the SG13G2 technology, the Magic extraction backend, and a capacitance-output threshold of 2 fF. Use the installed `kpex --help` to confirm option semantics for your version. Lowering the threshold retains smaller capacitances and is useful for checking sensitivity on the regenerative and input nodes. Do not assume that every extraction mode includes the same resistance and capacitance detail.

The relevant design files are:

| File under `$CMP7345_ROOT` | Role |
|----------------------------|------|
| `layout/klayout/CMP7345.gds` | Layout used for extraction |
| `netlist/schematic/CMP7345-final.spice` | Final schematic export |
| `netlist/pex/CMP7345.pex.spice` | Supplied extracted subcircuit |
| `netlist/pex/CMP7345.sym` | Dedicated Xschem symbol for the extracted view |
| `testbenches/tran/xschem/CMP7345_pex_tb.sch` | Post-layout transient testbench |

When generating a new extracted view, point the bench at the newly generated file and retain its extraction log. Otherwise, it is easy to compare a revised layout against an older PEX netlist.

## Prepare the PEX Testbench

```bash
cd "$CMP7345_ROOT/testbenches/tran/xschem"
xschem CMP7345_pex_tb.sch
```

The pinned upstream bench references its PEX symbol through a machine-specific absolute path. In your exercise copy, replace that symbol reference with the local file:

```text
$CMP7345_ROOT/netlist/pex/CMP7345.sym
```

Expand `$CMP7345_ROOT` to the actual directory when selecting the symbol in Xschem. This PEX symbol has `type=primitive`, so the comparator comes from the included SPICE subcircuit. It differs from the schematic symbol of the same filename.

The model block must include the extracted netlist. Set the include to the actual extracted file; for the supplied netlist, an Xschem model block using `format="tcleval( @value )"` can contain:

```spice
.include "$::env(CMP7345_ROOT)/netlist/pex/CMP7345.pex.spice"
```

Check the generated deck to confirm that Tcl expanded the path. The upstream relative include assumes a particular simulation output directory, so verify it whenever changing the netlisting location.

### Check the Interface

The stored schematic and extracted views have different port orders:

| View | Port order |
|------|------------|
| Stored final schematic export | `v- v+ vss vdd clk vout2 vout1` |
| Supplied PEX subcircuit `CMP7345` | `vdd vout1 vout2 v+ v- clk vss` |

Use the dedicated PEX symbol and confirm that its generated instance follows the extracted `.subckt` declaration. Read the actual declarations after every re-export rather than relying on a previous port order.

For the supplied extracted view, a testbench instance using `vp` and `vm` as its input node names has this order:

```spice
Xcmp vdd vout1 vout2 vp vm clk vss CMP7345
```

The sequence follows `.subckt CMP7345 vdd vout1 vout2 v+ v- clk vss`. A positional call copied from the stored final schematic export would connect the wrong nets. Inspect the generated instance and its model include before running the simulation.

### Compare Devices and Connectivity

| Check | How to interpret it |
|-------|---------------------|
| Tail device | Sum the widths of parallel extracted fingers and compare them with the intended 6 µm tail width. |
| Input and NMOS regenerative pairs | Identify the active units on each branch and compare effective width/length with the final schematic. |
| PMOS regenerative sources | Confirm both source-side networks reach the intended supply after hierarchy is flattened. |
| Body/tap networks | Check how local body connections and protection structures are represented by the extractor. |
| Added capacitors | Identify which nodes are loaded or coupled and whether the two branches remain balanced. |

A larger number of transistor instances can be normal finger expansion. A different effective width or a genuinely disconnected supply is an implementation discrepancy. Use the LVS results and extracted connectivity to distinguish these cases before interpreting performance.

## Compare Schematic and Extracted Results

1. Select the **final** schematic view for the pre-layout baseline as described in [Part 1](../part_1_schematic/README.md).
2. Match input stimulus, supply, clock, output loads, numerical options, and measurement definitions between the two benches. The supplied nominal and PEX benches have different input-ramp amplitudes.
3. Re-run both input polarities and inspect precharge, regeneration, output swing, and clock-to-output delay.
4. Re-check kickback using the same input-source network as in Part 2.
5. Investigate large changes in reset or decision polarity through pin mapping and connectivity before attributing them to capacitance.

Keep a small comparison table:

| Measurement | Final schematic | PEX | Explanation |
|-------------|-----------------|-----|-------------|
| Clock-to-output delay | Measured value | Measured value | Added loading or a changed current path |
| Reset completeness | Observation | Observation | Precharge time and branch balance |
| Differential kickback | Measured value | Measured value | Input coupling and source impedance |
| Near-zero-input decision | Observation | Observation | Regeneration margin and asymmetry |

The extracted waveform need not exactly reproduce the schematic waveform. The goal is to explain the differences and establish whether the implementation meets the selected functional and timing requirements.

### Interpret Differences Systematically

- **Delay increases but polarity remains correct:** compare the added loading, clock waveform, and early `P/Q` separation. Repeat with a smaller numerical time step to separate physical and numerical effects.
- **A branch no longer resets:** inspect precharge connectivity, clock timing, and the extracted capacitance on that branch.
- **Decision polarity reverses for a large input:** inspect pin mapping and cross-coupled connectivity first.
- **Only near-zero inputs change:** examine branch imbalance, numerical sensitivity, and the time allowed for resolution.
- **Kickback changes:** compare coupling paths and source impedance; added layout coupling can change both the peak and its settling time.

After the nominal comparison, repeat selected process/supply conditions and input-common-mode points. If running mismatch on an extracted view, first verify that the extracted device instances support the relevant model parameters. Do not assume the schematic's mismatch-enable settings were transferred automatically.

### Exercise Outcome

Keep the extraction settings and netlist, the checked PEX symbol/pin mapping, and the pre-/post-layout comparison table. Explain which differences are caused by parasitics and which require a schematic or layout correction. Use the resulting implementation as the starting point for chip finishing.
