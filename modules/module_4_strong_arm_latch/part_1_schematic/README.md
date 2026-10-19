# Part 1 – Architecture and Schematic Capture

[Module overview](../README.md) · [Next: Simulations](../part_2_simulations/README.md)

The StrongARM latch combines a differential input pair with a clocked current path and cross-coupled regenerative devices. It is useful in data converters because the core draws no intentional static current during reset and rapidly amplifies a small input difference during evaluation.

## Read the Architecture

![Basic StrongARM schematic](../.media/schem-basic.png)

| Devices | Role |
|---------|------|
| `M1/M2` | Input differential pair: converts the input difference into unequal discharge currents; a major input-offset contributor. |
| `M3/M4` | NMOS cross-coupled pair: contributes to the discharge and regeneration paths. |
| `M5/M6` | PMOS cross-coupled pair: positive feedback drives the decision toward the supply rails. |
| `M7` | Clocked tail switch: enables evaluation and influences speed, energy, and kickback. |
| `MS1–MS4` | Reset switches: precharge internal nodes and outputs before the next comparison. |

### Reset and Evaluation

1. **Clock low – reset:** the tail switch is off and the PMOS reset switches precharge the internal nodes. The two branches should begin the next comparison in equivalent states.
2. **Clock high – evaluation:** the tail path turns on. A differential input produces unequal discharge rates; the cross-coupled devices then regenerate that imbalance into a full decision.
3. **Next reset:** the raw comparator outputs return to the precharge state. A following SR latch can retain the decision between comparisons. Output inverters alone provide buffering, not memory.

Incomplete reset creates a dependence on the previous decision. Unequal output loading can create a systematic preference even with nominally matched input devices.

### Follow a Positive Input Difference

Define the input difference as $V_{diff}=V_+-V_-$. With $V_{diff}>0$, `M1` initially conducts more strongly than `M2`, so `P` discharges faster than `Q`. This imbalance develops before the cross-coupled structure makes a large-signal decision. In the supplied basic schematic, the resulting decision drives `vout1` low and `vout2` high; the output inverter then makes `IsHigh` high.

The early amplification is important for offset. An error introduced by the input pair acts before useful gain has developed. Errors introduced later by the cross-coupled pairs are partially reduced when referred back to the input. This is why matching effort should begin with the input pair, even though every pair participates in regeneration.

The same mechanism also explains metastability: when the initial imbalance is very small, regeneration needs longer to produce a valid output. A single-phase clock and a compact dynamic core are attractive, but timing, offset, and disturbance of the input source must be considered together.

## Open and Capture the Schematic

Use the environment variables from the [module setup](../README.md#get-the-design-and-set-up-paths):

```bash
cd "$CMP7345_ROOT/schematic/xschem"
xschem CMP7345-basic.sch
```

Identify `P`, `Q`, `clk`, `v+`, `v-`, `vout1`, and `vout2`. Trace the reset and evaluation current paths before editing sizes. For the guided exercise, draw the core yourself and use this file as the reference.

Useful Xschem shortcuts are:

| Key | Action |
|-----|--------|
| `q` | Open the selected object's properties. |
| `m`, `c` | Move or copy a selected object. |
| `Alt+R`, `Alt+F` | Rotate or flip a symbol. |
| `w` | Draw a wire. |
| `Delete` | Remove a selected object. |
| `Shift+A` | Inspect the generated netlist. |

### Optional Tool Warm-Up

For the two-day format, begin with a capacitive-resistive divider. This introduces sources, labels, grounding, netlisting, and waveform inspection before adding transistor models.

1. Place `vsource`, two `res` symbols, two `capa` symbols, and `gnd` from Xschem's device library.
2. Connect `R1` from the source node `Vin` to `Vdiv`, and `R2` from `Vdiv` to ground.
3. Put `C1` across `R1` and `C2` across `R2`.
4. Use `lab_wire` to name `Vin` and `Vdiv`.
5. As an example, set `R1=R2=10k`, `C1=1n`, and `C2=2n`.

With a constant input, the capacitors are open circuits and:

$$V_{div,DC}=V_{in}\frac{R_2}{R_1+R_2}$$

For a fast input step, the initial change follows the capacitive divider:

$$\Delta V_{div}(0^+)=\Delta V_{in}\frac{C_1}{C_1+C_2}$$

The complete small-signal transfer is:

$$\frac{V_{div}(s)}{V_{in}(s)}=
\frac{1/R_1+sC_1}{1/R_1+1/R_2+s(C_1+C_2)}$$

For the example values, the high-frequency ratio is $1/3$, the DC ratio is $1/2$, and the settling time constant is $(R_1\parallel R_2)(C_1+C_2)=15\,\mu s$. If you instead make $R_1C_1=R_2C_2$, the ideal divider ratio becomes independent of frequency.

Use a 1.2 V DC source and this control block to check the operating point:

```spice
.control
op
print v(Vdiv)
.endc
```

Then set the source to `PULSE(0 1.2 1u 10n 10n 150u 300u)` and replace the control block with:

```spice
.control
tran 1u 100u 0 10n
plot v(Vin) v(Vdiv)
write divider_tran.raw
.endc
```

The final `10n` limits the internal time step so that the fast edge can be inspected. Check the approximately 0.4 V initial response and the subsequent approach to 0.6 V. For AC analysis, give the source an AC magnitude of 1 and run `ac dec 100 10 100meg`; plot the magnitude and phase of `v(Vdiv)`. This linear example shows what AC analysis can reveal before moving to the clocked, nonlinear latch.

## Build the Comparator Core

Create an exercise schematic in the same configured Xschem directory and use the basic schematic as a reference. Add `sg13g2_pr/sg13_lv_nmos.sym` and `sg13g2_pr/sg13_lv_pmos.sym`, then enter the dimensions in the next section.

### Step 1 – Input Pair and Tail

- Connect the gates of `M1` and `M2` to `v+` and `v-`.
- Label their drains `P` and `Q`.
- Join their sources at the tail node; connect that node to the drain of `M7`.
- Connect the gate of `M7` to `clk` and its source to `vss`.
- In the basic view, connect all NMOS bulk terminals to `vss`.

### Step 2 – Cross-Coupled Devices

Use the following connections to make the feedback explicit. The table lists **drain, gate, source, bulk** in that order:

| Device | Drain | Gate | Source | Bulk |
|--------|-------|------|--------|------|
| `M3` | `vout1` | `vout2` | `P` | `vss` |
| `M4` | `vout2` | `vout1` | `Q` | `vss` |
| `M5` | `vout1` | `vout2` | `vdd` | `vdd` |
| `M6` | `vout2` | `vout1` | `vdd` | `vdd` |

The gates of the NMOS and PMOS devices on one branch are controlled by the opposite branch's output. Check these connections in the generated netlist as well as in the drawing.

### Step 3 – Precharge Switches and Ports

Add four PMOS switches with their gates connected to `clk` and their sources/bulks connected to `vdd`. Their drains precharge `P`, `Q`, `vout1`, and `vout2`, respectively. These switches restore internal conditions each time the clock is low.

Add ports named `v+`, `v-`, `clk`, `vdd`, `vss`, `vout1`, and `vout2`. Generate a symbol using **Symbol → Make symbol from schematic**, then inspect its port names and order. Netlist a small testbench instance and compare its positional connections with the generated `.subckt` declaration.

## Starting Sizes and Trade-Offs

The basic CMP7345 design uses the following dimensions. Widths are the total width of each transistor, not an extra factor to multiply by `ng`.

| Devices | Width | Length | Implementation note |
|---------|-------|--------|---------------------|
| `M1/M2` | 8 µm each | 0.26 µm | Final view uses eight 1 µm unit devices per side. |
| `M3/M4` | 8 µm each | 0.26 µm | Final view uses eight 1 µm unit devices per side. |
| `M5/M6` | 4 µm each | 0.26 µm | Final view uses four 1 µm unit devices per side. |
| `M7` | 6 µm | 0.13 µm | Six gate fingers. |
| `MS1–MS4` | 3 µm each | 0.13 µm | Three gate fingers per switch. |

Pelgrom-style reasoning provides a first estimate of matching area:

$$\sigma(\Delta V_{TH}) \approx \frac{A_{VTH}}{\sqrt{WL}}$$

Current-factor mismatch follows a similar area dependence:

$$\sigma\left(\frac{\Delta\beta}{\beta}\right)\approx\frac{A_\beta}{\sqrt{WL}}$$

Use coefficients consistent with the PDK and the definition of pair mismatch. Generic technology rules of thumb are useful for intuition but do not replace the process models. At fixed length, doubling the device width reduces this first-order random mismatch estimate by $1/\sqrt{2}$ while increasing gate and junction capacitances.

Larger input devices can reduce random threshold mismatch but add capacitance. A stronger tail switch can reduce delay while increasing switching disturbance. Stronger reset devices improve precharge but add clock loading. Change one group at a time and measure the effects in Part 2.

Use the low-millivolt offset and high-speed objectives from the module overview to guide these choices, then establish actual performance by simulation. Minimum length is a useful starting point for switches; the input and regenerative pairs use longer channels here to provide matching area. Document effective width, number of fingers, and parallel multiplicity separately so that the layout and schematic remain comparable.

## Preserve the Output Between Decisions

The comparator's raw outputs both precharge high during reset. The output inverters in the supplied testbench therefore both return low, which removes the previous digital decision.

A cross-coupled NAND SR latch can retain the result when driven by the raw active-low outputs: both latch inputs high means hold, while one low input selects a state. Verify the required polarity against the actual comparator outputs before connecting it. An output-memory exercise should check:

- Correct capture of positive and negative input differences.
- Retention through the next comparator reset phase.
- Balanced loading of the two comparator outputs.
- Additional comparator-to-memory delay and behavior near unresolved decisions.

The provided benches use output inverters. Adding the memory element is a separate extension, and its load must be included when repeating the timing measurements.

## Move to the Layout-Compatible View

```bash
cd "$CMP7345_ROOT/schematic/xschem"
xschem CMP7345-final.sch
```

![Layout-compatible StrongARM schematic](../.media/schem-final.png)

The final view introduces `diff_pair`, `cc_pair_nmos`, and `cc_pair_pmos` subcircuits, unit devices, dummies, local taps, and protection structures. Match each sub-block to the architectural transistor pair, keeping effective width and bulk connections explicit.

The testbenches instantiate `CMP7345.sym`, which opens `CMP7345.sch`. In the pinned design, `CMP7345.sch` is a symbolic link to `CMP7345-basic.sch`. Use the basic view for the initial simulation exercises. When validating the layout-compatible circuit, switch that link to `CMP7345-final.sch` in your exercise checkout and regenerate the netlist. Record the selected view with each result.

### Exercise Outcome

- Explain the role of each transistor group and the two clock phases.
- Produce a readable, symmetric schematic with named internal nodes and correct supply/bulk connections.
- Inspect the generated netlist and identify the selected schematic view, effective device widths, and symbol pin order.
- Explain why a separate output memory element may be needed.
