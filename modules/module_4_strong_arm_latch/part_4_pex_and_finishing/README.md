# Part 4 – Parasitic Extraction and Chip Finishing

[Previous: Layout](../part_3_layout/README.md) · [Module overview](../README.md)

Parasitic extraction (PEX) adds the interconnect loading that is missing from the ideal schematic. In a dynamic latch, this can change regeneration delay, reset balance, input disturbance, and the minimum input difference that resolves within the available time.

## Extract the Comparator

After the DRC/LVS work in Part 3, run the workshop's Magic-based extraction through KLayout-PEX. Use the [module environment](../README.md#get-the-design-and-set-up-paths):

```bash
cd "$CMP7345_ROOT/layout/klayout"
kpex --pdk ihp-sg13g2 --magic --magic_cthresh=2.0 --gds CMP7345.gds
```

Inspect the extraction log for the generated SPICE file and output directory. Compare it with the supplied `netlist/pex/CMP7345.pex.spice`. Record the extraction options, especially the capacitance threshold, when comparing results.

## Prepare the PEX Testbench

```bash
cd "$CMP7345_ROOT/testbenches/tran/xschem"
xschem CMP7345_pex_tb.sch
```

The pinned upstream bench references its PEX symbol through an absolute path from the author's machine. In your exercise copy, replace that symbol reference with the local file:

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

The workshop comparison notes identify different port orders:

| View | Port order |
|------|------------|
| Stored final schematic export | `v- v+ vss vdd clk vout2 vout1` |
| Supplied PEX subcircuit `CMP7345` | `vdd vout1 vout2 v+ v- clk vss` |

Use the dedicated PEX symbol and confirm that its generated instance follows the extracted `.subckt` declaration. Read the actual declarations after every re-export rather than relying on a previous port order.

Also compare the effective tail-device width and the PMOS pair's supply connections. The workshop's earlier comparison notes raised questions about these items; use the current netlist and LVS results to determine whether a difference is a real mismatch, a device-finger expansion, or a naming change.

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

## Chip Finishing

The comparator is a core block. Chip-level integration adds the surrounding structures and process checks needed for a complete design.

The workshop introduces **dummy fill** to improve density uniformity and **a sealring** at the final chip boundary. Keep the sealring in the chip-level context; it is not a ring to add around every comparator instance.

For the finishing exercise:

1. Use an exercise copy of the layout and define the intended chip-level context, including the sealring.
2. Run KLayout's SG13G2 **Fill Activ/GatPoly**, **Fill Metal**, and **Fill Top Metal** actions as appropriate for the target process.
3. Run **Density Report** and inspect the result.
4. Re-run DRC with density checking enabled, using the PDK's default rules.
5. Revisit extraction and post-layout simulation when the added fill changes the sensitive nodes' parasitic environment.

See the [IHP filler-generation documentation](https://ihp-open-pdk-docs.readthedocs.io/en/latest/finishing/filler.html) for the scripted flow and process-specific fill settings. The comparator's Metal1–Metal3 routing constraint and the chip-level fill requirements serve different purposes; follow the selected process rules for finishing.

## Optional Extension – PVT and Design Improvements

The workshop includes PVT characterization as a bonus topic. Extend the measurements across supported **process, voltage, and temperature** conditions, keeping the same timing and logic-level criteria. Automating this matrix with a characterization tool such as CACE is an additional exercise.

Further design studies from the manual include enlarging the input pair, adding drain equalization during reset, evaluating common-mode sensitivity, and investigating a preamplifier. For each change, compare offset, delay, and kickback together rather than optimizing only one metric.

### Exercise Outcome

Keep the extracted netlist, the checked PEX symbol/pin mapping, the comparison table, and the finishing observations. Finish with a short explanation of the dominant speed/offset/kickback trade-off in your implementation.
