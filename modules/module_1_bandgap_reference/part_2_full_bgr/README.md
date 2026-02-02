# Designing the Bandgap Reference

In this tutorial, we will design a functional bandgap reference circuit and perform the necessary simulations to evaluate its performance. Our analysis will cover both the DC characteristics and transient behavior of the bandgap reference. Additionally, to understand the effects of mismatch, we will delve into the concept of mismatch analysis and conduct Monte Carlo simulations. Unlike the traditional BJT-based reference discussed in the introduction, the circuit we will design here uses an all-CMOS implementation. This approach leverages transistors M1 and M2 operating in weak inversion to achieve the desired performance.

<p align="center"> <img src=".media/CMOS_bandgap.png" width="1000" height="900" /> </p>


In the schematic above, we observe an all-CMOS bandgap reference circuit, which we will design in the following tutorial. As previously discussed in the introduction, achieving a temperature-dependent characteristic is essential to generate a CTAT (Complementary to Absolute Temperature) behavior in terms of current.

For an NMOS transistor operating in the weak inversion (subthreshold) region, the current exhibits an exponential dependence on VGS​. This makes the NMOS transistor suitable for generating a CTAT characteristic, particularly because VGS​ varies with temperature.

<p align="center"> <img src=".media/vgs_cmos.png" width="1000" height="900" /> </p>

Similarly, by exploiting the voltage difference between the VGS​ values of transistors M1​ and M2​, we can generate a PTAT (Proportional to Absolute Temperature). 


### Challenges of Using Resistors in CMOS Technology

Designing with resistors in CMOS technology involves several challenges that can impact circuit performance. One key issue is **temperature dependence**, as resistors often experience changes in resistance due to temperature variations, which can affect precision in analog and mixed-signal circuits. This is especially problematic in resistors with high temperature coefficients (TCs), leading to variability under different operating conditions.

**Area constraints** are also a concern, as achieving high resistance values requires larger resistor dimensions, consuming valuable chip space. This creates a trade-off between resistance and area efficiency, especially in dense designs. Below we will discuss the resistors available in the SG13G2 PDK
.
### **Resistor Types in SG13G2 PDK**

The SG13G2 process provides three primary resistor types, each tailored for specific use cases:

1. **Rsil (Salicided n-doped Polysilicon Resistor)**:
    
    - **Material**: Salicided, n-doped polysilicon.
    - **Characteristics**:
        - Low sheet resistance (7 Ω/□7 \, \Omega/\square7Ω/□).
        - High temperature coefficient (TC: 3100 ppm/K3100 \, \text{ppm/K}3100ppm/K).
    - **Applications**:
        - Suitable for low-resistance paths but not ideal for precision or temperature-sensitive applications.
2. **Rppd (Unsalicided p-doped Polysilicon Resistor)**:
    
    - **Material**: Unsalicided, p-doped polysilicon.
    - **Characteristics**:
        - Moderate sheet resistance (260 Ω/□260 \, \Omega/\square260Ω/□).
        - Low temperature coefficient (TC: 170 ppm/K170 \, \text{ppm/K}170ppm/K).
    - **Applications**:
        - Ideal for precision applications and temperature-sensitive designs.
3. **Rhigh (High-Resistance Structures)**:
    
    - **Material**: Specialized high-resistance structures.
    - **Characteristics**:
        - Extremely high sheet resistance (exact values depend on design and material).
        - Temperature behavior varies with structure.
    - **Applications**:
        - Used for high-impedance paths and circuits where area and power constraints allow.


| **Resistor Type** | **Material**                 | **Sheet Resistance**   | **Temperature Coefficient (TC)** | **Applications**                        |
|-------------------|------------------------------|-------------------------|-----------------------------------|-----------------------------------------|
| Rsil              | Salicided n-doped polysilicon | 7 Ω/□                  | 3100 ppm/K                       | Low-resistance paths, non-precision use |
| Rppd              | Unsalicided p-doped polysilicon | 260 Ω/□               | 170 ppm/K                        | Precision and temperature-sensitive designs |
| Rhigh             | High-resistance structures    | Very high              | Variable                         | High-impedance paths                    |

Rppd’s low temperature coefficient, good precision, and moderate resistance make it ideal for bandgap reference circuits. It ensures temperature stability, process consistency, and area efficiency. Lets build the schematic

### 1. Building the Schematic

First, we will build the core of the bandgap reference.

<p align="center"> <img src=".media/bandgap_core.png" width="1000" height="700" /> </p>

As shown here, the setup is quite basic. You can adjust it to your needs, as long as the proper connections are maintained. The new component introduced is the RPPD resistors, which can be found in the components library under the PDK directory. Ensure the device sizes match those shown in the image, and don't forget to add a voltage source to supply VDD.


### Verilog-A Model for the Differential Amplifier (Outdated)
At this point we want to introduce the concept of an ideal amplifier. We will create this in Verilog A. Verilog-A allows for the behavioral modeling of analog circuits, enabling efficient testing and simulation. The `openvaf` compiler is used to convert the Verilog-A description into a format usable by simulation tools.

#### Creating the Verilog-A Model

First, create a `verilog` directory in the repository and define a file named `diff_amp.va`. The following Verilog-A code describes the differential amplifier:

```
// importing libs

`include "discipline.h"

module diff_amp (out, IN1, IN2);

output electrical out; 

input electrical IN1, IN2;

parameter real gain = 10; // setting gain to 10 of the differential amplifier

analog begin

    V(out) <+ gain * (V(IN1) - V(IN2));

end

endmodule

```

**Explanation:**

- The `discipline.h` file provides definitions for electrical signals.
- The module `diff_amp` has one output (`out`) and two inputs (`IN1` and `IN2`).
- A parameter `gain` allows the amplifier gain to be specified (default is 10).
- The `analog` block implements the core behavior, where the output voltage is the product of the gain and the input voltage difference.

#### Verifying the Model with a Testbench

To verify the functionality of the Verilog-A module, create a testbench file (`tb_diff_amp.sch`) and simulate it. Begin by compiling the Verilog-A code using `openvaf`:

```
openvaf /path/to/verilog/diff_amp.va
```
This generates an `.osdi` file that is required for simulation. The symbol for the differential amplifier can be accessed using `diff_amp.sym`, and its properties can be viewed by pressing `q` in the symbol editor. The relevant section includes:
```
type=opamp_va
format="@spiceprefix@name @@OUT @@IN1 @@IN2 @model"
template="name=U1 model=diff_amp_cell spiceprefix=X"

device_model="tcleval(
.subckt diff_amp_cell OUT IN1 IN2
N1 out in1 in2 diff_amp_model
.ends diff_amp_cell
.model diff_amp_model diff_amp

.control

* following line specifies the location for the .osdi file so ngspice can use it.
pre_osdi /IHP-AnalogAcademy/verilog/diff_amp.osdi
.endc

)"

```
#### Testbench Creation

Refer to the `tb_diff_amp.sch` file in the repository for an example of how to create a schematic-based testbench using this Verilog-A module. The testbench verifies the module's behavior. Remember to use the openvaf_23_5_0_linux_amd64.tar.gz for compiling the model, otherwise you will face convergence issues.

### 4. Inserting the Amplifier with Startup Circuitry

At this stage, you have two options for proceeding with the bandgap reference design:

1. **Using an Ideal Amplifier**:  
    You can create a bandgap reference with an ideal amplifier, as introduced earlier. This approach allows you to experiment with properties like the power supply rejection ratio (PSRR) and observe the effects of an arbitrarily high-gain amplifier.
    
2. **Using the OTA Designed in Part 1**:  
    To keep this tutorial concise, we will use the operational transconductance amplifier (OTA) designed in Part 1. This provides a practical implementation..
    

The circuit, including the amplifier and startup circuitry, is shown in the image below. Ensure proper connections as depicted. Refer to the next section for details on setting up the testbench.

<p align="center"> <img src=".media/OTA_amp.png" width="1000" height="600" /> </p>


## Bandgap Reference Testbench

The purpose of the testbench is to evaluate the performance of the bandgap reference circuit under various conditions. The primary goal of a bandgap reference is to maintain a stable voltage across a wide temperature range and respond predictably to changes in supply voltage (VDD). In this section, we will set up a **DC simulation profile** to analyze temperature stability and a **transient simulation profile** to examine the circuit's dynamic behavior.

### Importing Device Models

To perform accurate simulations, we first include the model libraries for resistors, transistors, and capacitors. This ensures that the simulation reflects real-world component behavior. Create and insert the following code block for importing the necessary models:
```
name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib cornerMOSlv.lib mos_tt
"
```
### Setting Up the Simulation Profile

Next, create the simulation profile for the DC analysis. This profile focuses on evaluating the reference voltage's stability across a temperature range from -50°C to 100°C. Insert the following code block to configure the DC simulation:

```
"
.control
.save all
alter V1 dc 1.2            
op
dc TEMP -50 100 5
write bgr_temp.raw
.endc

```
### Setting Up the Transient Simulation Profile

Transient simulation evaluates how the circuit reacts to time-varying conditions, such as a ramped supply voltage. This step ensures the bandgap reference circuit stabilizes at the desired voltage in a realistic startup scenario. Use the following code block to define the transient simulation:

```
.control
.save all     
tran 1m 2 
write bandgap_transient.raw
.endc


"
```

- **`tran 1m 2`**: Runs a transient analysis with a 1ms time step for 2ms total.
- **`write bgr_transient.raw`**: Exports the transient simulation data to a file (`bgr_transient.raw`)

### Voltage Source Configuration

For the transient simulation, the supply voltage source (`V1`) should simulate a realistic ramp-up. Use the following configuration:
Also the voltage source in the schematic should have the following value

```
"PULSE(0 1.2 0 1 0 1 2)"
```
**`PULSE(0 1.2 0 1 0 1 2)`**: Defines a pulse waveform that starts at 0V, ramps to 1.2V with a 1s rise time, and remains at 1.2V for 1s. This mimics a practical VDD ramp scenario during power-up. The general form of the pulse function is `PULSE(V1 V2 TD TR TF PW PER NP)`. General information about the ngspice simulator can be found in the following link: https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml


### Final Simulation Profile

Combine the DC and transient simulation profiles into one testbench as shown:

```
"
.control
.save all
alter V1 dc 1.2            
op
dc TEMP -50 100 5
write bgr_temp.raw
.endc

.control
.save all     
tran 1m 2 
write bgr_transient.raw
.endc

"
```
### Final Schematic

Ensure the schematic matches the design below:
<p align="center"> <img src=".media/final_bandgap_core.png" width="1000" height="500" /> </p>


### Visualizing Results

To visualize the results:

1. Import **two waveform viewers** as described in the previous tutorial.
2. Add **two launch buttons**, labeling them:
    - **Load DC** (for `bgr_temp.raw`).
    - **Load Transient** (for `bgr_transient.raw`).
3. Arrange the plots:
    - The top plot should display **VDD**.
    - The bottom plot should display **VBG** (bandgap reference voltage).


Expected results should resemble the following plots:

**Temperature Sweep (DC Simulation)**:
<p align="center"> <img src=".media/dc_temp_plot.png" width="1000" height="900" /> </p>

**Transient Analysis**:
<p align="center"> <img src=".media/tran_temp_plot.png" width="1000" height="900" /> </p>


### Mismatch and Monte Carlo Simulations

In real-world production, semiconductor devices like transistors are subject to variations in manufacturing processes. These variations, often referred to as **mismatch**, result from slight differences in dimensions, doping concentrations, and other fabrication parameters. Mismatch can have a profound impact on circuits that rely on symmetry and precision, such as **differential pairs**.

#### The Impact of Mismatch on Differential Pairs and Bandgap References

For example, in differential pairs, mismatch between the two transistors can result in imbalances in current distribution. This imbalance can compromise the accuracy, stability, and overall design integrity of the circuit if not properly addressed.

For a bandgap reference, mismatched devices can cause the reference voltage to deviate from its intended value. Even a small variation in key components, such as transistors or resistors, can shift the temperature coefficient or the nominal output voltage, leading to performance degradation.

### Why Monte Carlo Simulations Are Essential

To account for mismatch in circuit design, engineers perform **Monte Carlo simulations**, which introduce random variations to model the effects of mismatch statistically. These simulations help:

- Predict the impact of process variations on circuit performance.
- Identify design weaknesses sensitive to mismatch.
- Evaluate if the circuit meets specifications under worst-case conditions.
### Monte Carlo Simulation for Mismatch

In mismatch simulations, the tool generates a large number of circuit instances, each with random variations applied to components like transistors and resistors. For example, the threshold voltage Vth of transistors might vary slightly between runs.

#### Number of Runs: Industry Considerations

The number of runs required for a Monte Carlo simulation depends on several factors, including the desired confidence level and the complexity of the circuit. While **400 runs** is often cited as a typical benchmark in the industry to achieve statistically meaningful results, this number may vary. Smaller circuits or lower confidence requirements might allow for fewer runs, while highly sensitive or complex designs may require significantly more runs to capture outliers and ensure robust trend analysis.

---

### Understanding 3-Sigma Analysis

Monte Carlo simulation results are often evaluated using a **3-sigma (3σ)** approach:

- **1σ (1 standard deviation):** Captures ~68% of the data around the mean.
- **2σ (2 standard deviations):** Covers ~95% of the data.
- **3σ (3 standard deviations):** Encompasses ~99.7% of the data.

By analyzing at the 3σ level, designers can ensure that the circuit performs reliably under nearly all manufacturing conditions, even those that result in extreme variations. For example, in a bandgap reference, a 3σ analysis would verify that the reference voltage remains stable for 99.7% of possible mismatch scenarios. 

---

### Connecting to Bandgap Reference Design 

In the context of bandgap reference design, **Monte Carlo mismatch simulations** play a key role in:

- Assessing how device mismatch impacts the output voltage variation.
- Verifying that the design adheres to strict accuracy and temperature stability requirements.
- Determining if trimming or calibration is necessary to compensate for mismatch during production.

When considering the **3-sigma interval**, the focus shifts to evaluating the overall trend of the bandgap voltage across the temperature range. For this design, the critical objective is to ensure that even the most extreme scenarios fall within a stable voltage band, approximately centered around $Vdd/2$

The next section will demonstrate how to set up and perform a Monte Carlo simulation for the bandgap reference. This includes defining mismatch parameters, specifying the number of runs, and analyzing the results to assess robustness.

### Mismatch Monte Carlo simulation in xschem with ngspice (ongoing)
### Mismatch and Monte Carlo Simulations

In real-world production, semiconductor devices like transistors are subject to variations in manufacturing processes. These variations, often referred to as **mismatch**, result from slight differences in dimensions, doping concentrations, and other fabrication parameters. Mismatch can have a profound impact on circuits that rely on symmetry and precision, such as **differential pairs**.

#### The Impact of Mismatch on Differential Pairs and Bandgap References

For example, in differential pairs, mismatch between the two transistors can result in imbalances in current distribution. This imbalance can compromise the accuracy, stability, and overall design integrity of the circuit if not properly addressed.

For a bandgap reference, mismatched devices can cause the reference voltage to deviate from its intended value. Even a small variation in key components, such as transistors or resistors, can shift the temperature coefficient or the nominal output voltage, leading to performance degradation.

### Why Monte Carlo Simulations Are Essential

To account for mismatch in circuit design, engineers perform **Monte Carlo simulations**, which introduce random variations to model the effects of mismatch statistically. These simulations help:

- Predict the impact of process variations on circuit performance.
- Identify design weaknesses sensitive to mismatch.
- Evaluate if the circuit meets specifications under worst-case conditions.
### Monte Carlo Simulation for Mismatch

In mismatch simulations, the tool generates a large number of circuit instances, each with random variations applied to components like transistors and resistors. For example, the threshold voltage Vth of transistors might vary slightly between runs.

#### Number of Runs: Industry Considerations

The number of runs required for a Monte Carlo simulation depends on several factors, including the desired confidence level and the complexity of the circuit. While **400 runs** is often cited as a typical benchmark in the industry to achieve statistically meaningful results, this number may vary. Smaller circuits or lower confidence requirements might allow for fewer runs, while highly sensitive or complex designs may require significantly more runs to capture outliers and ensure robust trend analysis.

---

### Understanding 3-Sigma Analysis

Monte Carlo simulation results are often evaluated using a **3-sigma (3σ)** approach:

- **1σ (1 standard deviation):** Captures ~68% of the data around the mean.
- **2σ (2 standard deviations):** Covers ~95% of the data.
- **3σ (3 standard deviations):** Encompasses ~99.7% of the data.

By analyzing at the 3σ level, designers can ensure that the circuit performs reliably under nearly all manufacturing conditions, even those that result in extreme variations. For example, in a bandgap reference, a 3σ analysis would verify that the reference voltage remains stable for 99.7% of possible mismatch scenarios. 

---

### Connecting to Bandgap Reference Design 

In the context of bandgap reference design, **Monte Carlo mismatch simulations** play a key role in:

- Assessing how device mismatch impacts the output voltage variation.
- Verifying that the design adheres to strict accuracy and temperature stability requirements.
- Determining if trimming or calibration is necessary to compensate for mismatch during production.

When considering the **3-sigma interval**, the focus shifts to evaluating the overall trend of the bandgap voltage across the temperature range. For this design, the critical objective is to ensure that even the most extreme scenarios fall within a stable voltage band, approximately centered around $Vdd/2$

The next section will demonstrate how to set up and perform a Monte Carlo simulation for the bandgap reference. This includes defining mismatch parameters, specifying the number of runs, and analyzing the results to assess robustness.

### ### Monte Carlo Mismatch Simulation in Xschem: A Step-by-Step Tutorial (ongoing)

In this tutorial, we’ll demonstrate how to perform a Monte Carlo mismatch simulation in Xschem using a bandgap circuit as an example. This process involves introducing random variations in device parameters to analyze how mismatch affects the circuit's performance.

---
#### **Step 1: Importing Models**

To begin, include the appropriate model files in your simulation. For mismatch simulations, the models should include mismatch parameters. Use the following imports:

```
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ .lib $::SG13G2_MODELS/cornerRES.lib res_typ .lib cornerMOSlv.lib mos_tt_mismatch
```


- **`cornerCAP.lib`**: Includes typical capacitor models.
- **`cornerRES.lib`**: Includes typical resistor models.
- **`cornerMOSlv.lib`**: Includes MOSFET models with mismatch parameters (`mos_tt_mismatch`).

To perform statistical analysis instead of mismatch analysis, use the `mos_tt_stat` model. This captures wafer-to-wafer statistical variations.

#### **Step 2: Setting Up the Simulation**

The following code sets up the Monte Carlo mismatch simulation. This script performs multiple simulation runs, introduces variations, and records the results.

```
name=NGSPICE only_toplevel=false 
value="
.control
  let run = 1
  let mc_runs = 200
  set curplot = new
  set scratch = $curplot
  dowhile run <= mc_runs
    reset
    dc temp 100 -50 -5
    set run = $&run
    set dc = $curplot
    setplot $scratch
    let off{$run} = {$dc}.v(VBG)
    let mytemp{$run} = \"{$dc}.temp-sweep\"
    setplot $dc
    let run = run + 1
  end
  set nolegend
  plot {$scratch}.allv vs {$scratch}.mytemp1
  write bandgap_testbench_mc_mis.raw {$scratch}.allv {$scratch}.mytemp1
.endc
"
```
---
#### **Script Breakdown**

1. **Initialization**:
    
    - `let run = 1`: Initializes the run counter.
    - `let mc_runs = 200`: Sets the number of Monte Carlo runs to 200.
2. **Simulation Loop**:
    
    - **Reset for Each Run**: The `reset` command clears the simulation state.
    - **Temperature Sweep**: The `dc temp 100 -50 -5` command sweeps temperatures from 100°C to -50°C in 5°C steps.
    - **Result Collection**:
        - `off{$run}`: Stores the bandgap output voltage (`VBG`) for each run.
        - `mytemp{$run}`: Stores the temperature sweep for each run.
3. **Plotting**:
    
    - Results from all runs are saved into `$scratch`.
    - `plot {$scratch}.allv vs {$scratch}.mytemp1`: Plots the output voltage against the temperature.
4. **Output**:
    
    - Results are written to a `.raw` file for further analysis: `bandgap_testbench_mc_mis.raw`.


From the written raw file the output is then plotted in python to extract the following result

<p align="center"> <img src=".media/monte_carlo.png" width="700" height="500" /> </p>




