# Introduction to the Comparator

At the core of the Successive Approximation Register (SAR) Analog-to-Digital Converter (ADC) lies one of its most critical components—the **comparator**. Its primary role is to determine whether the analog input voltage is higher or lower than the DAC output during each bit trial. The precision and speed of this decision directly influence the overall accuracy and performance of the ADC.

Comparators can generally be divided into two categories: **static** and **dynamic**. Static comparators operate continuously with a constant bias current, which leads to high power consumption due to static power dissipation. This makes them less favorable for low-power applications.

In contrast, **dynamic comparators** are clock-controlled and only activate during a specific phase of the clock cycle. This on-demand behavior significantly reduces power consumption, making dynamic comparators ideal for energy-efficient SAR ADC implementations

However, with dynamic comparators, another challenge emerges: **input-referred offset voltage**, which is the primary contributor to decision errors in the comparison process. This offset originates from device mismatch during fabrication, such as variations in threshold voltage and transistor dimensions. Consequently, minimizing offset while maintaining low power is a critical design trade-off.

In this context, we will work with the following comparator structure:
<p align="center"> 
  <img src=".media/comparator.png" width="900" height="750" /> 
</p>

Link to Paper: [A 10-bit 50-MS/s SAR ADC With a Monotonic Capacitor Switching Procedure](https://ieeexplore.ieee.org/document/5437496)

Authors: [Ying-Zu Lin](https://ieeexplore.ieee.org/author/37292128800), [Guan-Ying Huang](https://ieeexplore.ieee.org/author/37400350600), [Soon-Jyh Chang](https://ieeexplore.ieee.org/author/37281064400), & [Chun-Cheng Liu](https://ieeexplore.ieee.org/author/37406600700)




## Building the Schematic

By now, you should be comfortable creating schematics in **xschem**. As such, the schematic diagram is provided with key design considerations rather than an exhaustive walkthrough. Below is the comparator schematic, along with the symbol created for the design:

<p align="center"> 
  <img src=".media/comparator_xschem.png" width="900" height="750" /> 
</p>


The transistor dimensions in the schematic (shown above, not in **xschem**) are as follows:

- **M1, M2**: $W = 32 \mu m$, $L = 0.2 \mu m$, $ng = 4$
    
- **M3, M4, M5, M6**: $W = 4 \mu m$, $L = 0.2 \mu m$
    
- **M8, M10**: $W = 4 \mu m$, $L = 0.2 \mu m$
    
- **M7, M9**: $W = 8 \mu m$, $L = 0.2 \mu m$
    
- **M11, M12**: $W = 18 \mu m$, $L = 0.3 \mu m$, $ng = 4$
    

From this schematic, the corresponding symbol was created as follows:
<p align="center"> 
  <img src=".media/sym_comp.png" width="900" height="750" /> 
</p>



## Comparator Testbench

With the comparator schematic and symbol in place, the next step is simulating its behavior. A testbench is created to analyze the transient response of the comparator. The connections for the comparator and the associated sources are shown below:

<p align="center"> 
  <img src="../../../media/module_3/transient_test_bench_comp.png" width="1000" height="450" /> 
</p>


VIn the simulation setup:

- **Vdd** is set to **1.2V**.
    
- The **bias voltage** is set to **0.6V**.
    
- The **clock** signal is defined as follows:
```
name=V1 value="PULSE(0 1.2 0 0 0 5N {period})"
```
- Here, `{period}` will be defined in the code block.
- In the [Ngspice doucmentation](https://ngspice.sourceforge.io/docs/ngspice-manual.pdf) the `PULSE` function is defined as:
```
PULSE(V1 V2 TD TR TF PW PER NP)
```
<p > 
  <img src=".media/v_pulse_params.png" width="350" height="200" /> 
</p>
    
- The **positive input** is given by:
```
"PULSE(595e-3 605e-3 0 tr 1S 1S)"
```
- The **negative input** is simply connected to the bias voltage (**0.6V**).

What is worth noticing is that the positive input voltage ramps linearly from 595 mV to 605 mV with a rise time of **tr**. The fall time and period are sufficiently high to be negligible in the simulation, so the pulse exhibits a pure linear ramp. For the input capacitors, we use a capacitance of **6.4pF** to simulate the total capacitance from the C-DAC. The **output capacitor** is estimated to be small, reflecting the capacitance seen at the gate of two transistors.

As usual, the following model block is instantiated for the simulation:

```
name=MODEL only_toplevel=false
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
"
```
The NGSPICE code block for the simulation setup is:

```
name=NGSPICE only_toplevel=false
value="
.control
op
.param clock = 100e6    ; 100 MHz clock
.param period = 1 / clock
.param num_cycles = 100  ; number of evaluation cycles
.param tr = num_cycles * period
tran 500p 1u
.save all
let vindiff = (v(vinp))-(v(vbias))
let clk = v(clk)
let vout = (v(outp))-(v(outm))
write output_file.raw
.endc
"
```
### Explanation of the Code

- The `control` block defines the simulation environment and sets up the operating point analysis (`op`).
    
- `clock = 100e6` sets a 100 MHz clock frequency.
    
- `period` is derived as the inverse of the clock frequency.
    
- `num_cycles = 100` sets the number of evaluation cycles, and `tr` calculates the time duration of these cycles.
    
- The `tran 500p 1u` line specifies the transient analysis with a step size of **500 ps** and a total time of **1 µs**.
    
- The `.save all` command saves all simulation results.
    
- The `vindiff` variable computes the voltage difference between the positive input (`vinp`) and the bias voltage (`vbias`).
    
- `clk` captures the clock signal.
    
- `vout` calculates the output voltage difference between the positive output (`outp`) and the negative output (`outm`).
    
- Finally, the results are written to a raw output file (`output_file.raw`).

Once the simulation runs, you can plot the output as described in previous modules. The expected result is shown below as `vout`:
<p align="center"> 
  <img src=".media/comparator_output_vout.png" width="800" height="550" /> 
</p>

As seen in the output, once the positive input voltage crosses the **0.6V** threshold (the bias voltage at the negative input), the comparator's output goes high.
## Mismatch Analysis of the Comparator

As mentioned earlier, mismatch analysis plays a crucial role in understanding the behavior of circuits, and the comparator is no exception. Specifically, in the context of an **ADC**, the **input-referred offset** is one of the most critical factors impacting the performance of the comparator. Any mismatch in the transistor devices can introduce variations in the comparator’s decision-making threshold, leading to errors in the conversion process. Since this offset is inherent to the comparator’s design, it is important to estimate the impact of this mismatch across a range of samples.

In an ADC, the comparator’s accuracy directly affects the precision of the successive approximation process. Even small variations in the comparator’s offset can result in significant errors in the final digital output, especially as the input voltage approaches critical decision points. Therefore, performing a **Monte Carlo (MC) analysis** of the comparator’s behavior helps estimate how variations in the transistor dimensions and other parameters influence the ADC’s performance over multiple instances of the comparator. This is essential for understanding the potential error margins in real-world conditions, where fabrication mismatches are inevitable.

Below is the schematic for the mismatch Monte Carlo (MC) analysis of the comparator:


<p align="center"> 
  <img src=".media/mc_analysis_tb.png" width="950" height="700" /> 
</p>
As you can see, this setup closely resembles the testbench used for the simple transient analysis. However, there are some important differences. The most notable change is that the positive input voltage is now represented as a slow ramp, defined as:


```
name=V2 value="PULSE(595e-3 605e-3 0 tr 1S 1S)"

```

Looking at the model includes, we see that now have defined the mismatch model

```
name=MODEL1 only_toplevel=false
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt_mismatch	
"
```
This model includes variations in transistor parameters to simulate the effects of mismatches in the fabrication process. These variations are then used to analyze the impact on the comparator’s behavior.

### Explanation of the MC Simulation Code

The following **Ngspice** code block defines the MC analysis and provides detailed steps for running the simulation over multiple iterations:

```
name=NGSPICE only_toplevel=false
value="
.control
  let run = 1
  let mc_runs = 100
  let results = unitvec(mc_runs)
  dowhile run <= mc_runs
    reset
    .param clock = 100e6    ; 100 MHz clock
    .param period = 1 / clock
    .param num_cycles = 200  ; number of evaluation cycles
    .param tr = num_cycles * period
    tran 300p 2u
    set run = $&run
    let vdiff = v(outp) - v(outm)
    
    meas tran cross_time WHEN vdiff = 0.6
    let vindiff = v(vinp) - v(vbias)
    meas tran offset_voltage_{$run} find vindiff at=cross_time
    let results[$run - 1] = offset_voltage_{$run}
    let run = run + 1
  end
  print results > offset_MC_analysis.txt
  write offset_MC_analysis.raw
.endc

"
```
Let's break this down step by step:

1. **Initialization**:
    
    - `let run = 1`: Sets the starting point for the MC analysis runs.
        
    - `let mc_runs = 100`: Defines that the simulation will run 100 iterations to capture the impact of random mismatches on the comparator's performance.
        
    - `let results = unitvec(mc_runs)`: Initializes an empty vector (`results`) to store the offset voltage from each Monte Carlo run.
        
2. **Monte Carlo Loop** (`dowhile run <= mc_runs`):
    
    - The loop iterates 100 times (as specified by `mc_runs`).
        
    - `reset`: Resets the simulation at the beginning of each iteration to avoid contamination from previous runs.
        
    - The simulation parameters (clock frequency, period, number of cycles, etc.) are defined as before.
        
3. **Transient Analysis**:
    
    - `tran 300p 2u`: Defines the transient analysis with a time step of 300 ps and a total time of 2 µs. This allows us to observe the comparator’s response over a sufficiently long period.
        
4. **Voltage Difference Calculation**:
    
    - `let vdiff = v(outp) - v(outm)`: Calculates the voltage difference between the output nodes (`outp` and `outm`).
        
    - `meas tran cross_time WHEN vdiff = 0.6`: Measures the time at which the output crosses the 0.6 V threshold (decision level for the comparator).
        
5. **Offset Voltage Measurement**:
    
    - `let vindiff = v(vinp) - v(vbias)`: Computes the voltage difference between the positive input and the bias voltage.
        
    - `meas tran offset_voltage_{$run} find vindiff at=cross_time`: Measures the input-referred offset voltage at the time the output crosses 0.6 V.
        
    - The offset voltage for each run is stored in `results[$run - 1]`.
        
6. **Loop Increment**:
    
    - `let run = run + 1`: Increments the loop counter to continue to the next Monte Carlo iteration.
        
7. **Output**:
    
    - `print results > offset_MC_analysis.txt`: Saves the results (the offset voltage measurements) to a text file (`offset_MC_analysis.txt`).
        
    - `write offset_MC_analysis.raw`: Writes the raw data to a file (`offset_MC_analysis.raw`)

From here the simulation can be run.

## Plotting the results
To visualize the results of the Monte Carlo mismatch analysis, a Python 3 script is provided under the following path: 

```
part_1_comparator/testbench/statistical_calculation
```
You can run the script from the terminal using:

```
python script.py <path_to_txt_file>

```
For the current case, the command would be:

```
python3 calculate_histogram.py ../simulations/offset_MC_analysis.txt
```

Upon execution, the script reads the data, performs basic statistical analysis, and outputs the following to the terminal:

```
Total samples: 100
Mean: 144.699 µ
Standard Deviation: 1.69508 m
Do you want to create a histogram plot? (y/n): y

```
If you respond with `y`, the script generates a histogram of the offset voltage distribution and saves it in a newly created folder called `histogram_plots`. An example of the resulting plot is shown below:
<p align="center"> 
  <img src=".media/monte_histo.png" width="900" height="750" /> 
</p>

This visualization allows for easy inspection of the variation in offset voltage due to mismatch. The reader is encouraged to experiment with transistor sizing and other design parameters—such as rise/fall time or bias currents—to observe their influence on standard deviation, mean offset, and overall comparator behavior, including power consumption and decision speed.
