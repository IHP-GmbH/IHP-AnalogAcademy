# Biasing and Stability
In this section, we will begin the design phase of the **Medium Power Amplifier (MPA)** using **QUCS-S** as our schematic capture tool. This part of the tutorial will guide you through the RF workflow with open-source tools, and we'll lay a solid foundation for exploring and navigating in **QUCS-S**.

Before we dive into the design, make sure that you have the latest version of **QUCS-S** installed and properly set up to work with our open PDK. For detailed instructions on the installation, refer to our Read the Docs guide:

[Read the Docs](https://ihp-open-pdk-docs.readthedocs.io/en/latest/index.html)

## Simple Navigation in QUCS-S

Start by setting up a file structure that suits your preferences, or simply replicate the structure from the current repository. Once that's done, launch **QUCS-S** by typing the following command into your terminal:

To start with create an file system that suits your needs and preferences (or simply copy the structure from the current repository) and launch QUCS-S. This can be done by simply writing

```
qucs-s 
```

If you want to open a specific file directly from the terminal, use the following command:

``qucs-s -i /path/to/file.sch
``

After executing this, you should see a blank schematic workspace. Take a moment to explore the interface and familiarize yourself with the layout before moving on.

## Common QUCS-S Shortcuts

To improve your workflow, it's helpful to get comfortable with keyboard shortcuts. You can find a list of the most commonly used **QUCS-S shortcuts** here:

[QUCS-S Shortcuts](https://qucs-help.readthedocs.io/en/0.0.18/short.html)

I encourage you to try out a few of them as you navigate around the interface.

## Creating the Initial Schematic

We’ll start by instantiating the **npn13G2** BJT, which is a commonly used transistor for this design. You can find it in the following library:

```
`libraries/User libraries/IHP_PDK_nonlinear_components/npn13G2`
```

Next, navigate to the **Components** pane in the vertical column on the left side of the window. Search for **DC Block** and **DC Feed** components, then add them to the schematic.

Now, add **two ideal resistors** from the **Lumped Components** category (**Resistors US**) and set their values to **50 ohms** to ensure proper impedance matching.

Next, search for **DC Voltage Source** and **two power sources**  and create a two port system with the power sources. For the placement of the DC voltage source look at the image below. For labeling press 'Ctrl+L'.



<p align="center"> <img src=".media/schematic_bias_1.png" width="800" height="500" /> </p>


Now, we need to set up our **analysis mode** and configure the necessary parameters to capture the circuit's behavior in the first step. This includes:

1. **DC Analysis** – Used to determine the transistor’s operating point and bias conditions.
2. **S-Parameter Analysis** – Evaluates how the circuit behaves in the frequency domain by analyzing its scattering parameters (S-parameters). This is crucial for understanding signal reflection, transmission, and overall RF performance.

To set up these simulations, navigate to the **Components** pane and search for **DC Simulation** and **S-Parameter Simulation** blocks. Drag them onto the schematic.

Additionally, we need to specify the **library directory** for the device model to ensure the correct transistor parameters are used. This is done using the **Include Script** block, which can be found in the same **Components** section.

Below is the recommended parameter setup for the **S-Parameter Simulation**:

```
SP2
Type=lin
Start=1Ghz
Stop=200Ghz
Point=200
```
This **S-Parameter (SP2) simulation block** is configured to analyze the frequency response of the circuit from **1 GHz to 200 GHz** using a **linear frequency sweep**. Here's a breakdown of the parameters:

- **Type = lin** → Specifies a **linear sweep**, meaning the frequency steps are evenly spaced between the start and stop values.
- **Start = 1 GHz** → The simulation begins at **1 GHz**, ensuring that we capture low-frequency behavior.
- **Stop = 200 GHz** → The simulation extends up to **200 GHz**, allowing us to observe high-frequency performance.
- **Points = 200** → The sweep consists of **200 frequency points**, providing a detailed view of the circuit’s response over the frequency range.

and for the DC simulation just leave it as it is. For the include script the text inside the box should be the following

```
.LIB cornerHBT.lib hbt_typ
```
## Initial Simulation

Now that we have set up the testbench, we need to define our first simulation objective. As mentioned earlier, we will not go into deep theoretical explanations of the amplifier topology, but instead, we will conduct well-structured simulations that align with the key analysis steps needed in the design process of this amplifier.

### Determining the Number of Fingers

The first design decision is selecting the number of fingers for our **npn13G2** BJT. This determines the **current-handling capability** of the transistor, which directly affects its **linearity**. However, increasing the number of fingers introduces trade-offs, such as **higher parasitics**, which can impact **matching constraints** and **gain performance**.

To begin, we set an initial bias voltage, such as **1V**, and run the simulation by pressing the **simulate** button next to the simulator selector pane (make sure you are using **ngspice**). Once the simulation is complete, we need to analyze key parameters to determine the optimal bias point and transistor size.

### Setting Constraints

In the **SG13G2** technology, the **npn13G2** transistor has a maximum **current per finger** of **3.5 mA**. To evaluate the **collector current**, follow these steps:

1. **Insert a Current Probe**:
    - Search for **Current Probe** under **Components**.
    - Place it in **series** with the collector branch of the transistor.
2. **Create a New Analysis Window (.dpl Format)**:
    - To keep the testbench clean, open a new **.dpl** window to analyze results.
    - This format is used to display simulation data visually.
    - Click the **button with the following icon** (insert icon) to create it.
      <img src=".media/dpl_window.png" width="30" height="30" /> </p>
3. **Add Visualization Elements**:
    - Navigate to the **Diagram** tab under **Components** and insert:
        - **Smith Chart** → Used to analyze **reflection coefficients** (**S11** and **S22**), which provide insight into the necessary impedance matching (ac.v(s_1_1),  ac.v(s_2_2)).
        - **Tabular View** → Displays **DC information**, such as node voltages and currents.
        - **Cartesian Plot** → Used to plot the **K stability factor**, which ensures unconditional stability.
4. **Define the Stability Factor Expression (K-Factor)**:
    - Click **Insert Expression** from the top menu.
    - Add the following equation in the schematic:
```
K = (1 - abs(s_1_1)^2 - abs(s_2_2)^2 + abs(s_1_1 * s_2_2 - s_1_2 * s_2_1)^2) / (2 * abs(s_1_2 * s_2_1))
```

When these steps are done, your schematic should look like the following:
(remember to set the frequency in the elements that need it as we go !)
And you results/.dpl file should look like the following:
<p align="center"> <img src=".media/schematic_bias_2.png" width="800" height="600" /> </p>
(remember to set the frequency in the elements that need it as we go !)
And you results/.dpl file should look like the following:
<p align="center"> <img src=".media/results_bias_1.png" width="800" height="500" /> </p>
At this point we can add markers to the lines in order to analyze the results more precisely. 

## Finding the Optimal Number of Fingers

As previously mentioned, increasing the **current handling** of the BJTs improves **linearity**, but it also affects the **stability** of the circuit. To ensure the amplifier remains **unconditionally stable**, we must satisfy the **stability condition** where the **K factor** is greater than **1**.

When adjusting the **number of fingers**, we also have the flexibility to **fine-tune the base bias voltage** to find an optimal operating point. A good starting point is setting the **number of fingers to 10** and adjusting **bias to approximately 0.97V**, which results in a **total current of around 26mA** . This ensures a reasonable trade-off between **linearity, power consumption, and stability**.


## Playing around

At this stage we can try to play around with the stability of the amplifier. For this the schematic can be seen below. NOTE the tuning of the degenerative resistor and capacitor on the base is a loop, since it depends on many parameters. Below the initial approach can be seen
## Stabilizing the Amplifier

To improve **stability**, we introduce a base resistance in parallel with a capacitor. This provides a low frequency attenuation while allowing our frequency of interest. This helps introduce more stability to our circuit by degeneration. 

### Setting Up parameter for the inductor

To make tuning easier, we will define the **resistor value as a parameter**. This allows us to **easily adjust its value** during simulations. Follow these steps:

1. **Instantiate a `.Param` section**:
    - This block is found under **Equations**.
    - It allows us to define and modify circuit parameters dynamically.
2. **Define the starting value**:
    - Set an initial value (e.g., **Rstab =10k Ohm**).
    - This will act as our first guess before fine-tuning through simulation.

Once these steps are completed, your schematic should look like the following:
<p align="center"> <img src=".media/schematic_bias_3.png" width="800" height="600" /> </p>
## Simulating and Fine-Tuning

Now that the circuit is set up, we can proceed with the **simulation** and visualization of key parameters. Instead of using a **.dpl file**, we will directly add a **Smith chart** and a **Cartesian plot** to the testbench. These will allow us to observe:

- **S11 and S22**: Reflection coefficients, which indicate the input and output matching.
- **K-factor**: A stability metric that ensures the amplifier remains unconditionally stable (**K > 1**).
### Tuning the Inductor for Optimal Stability

1. **Launch the tuner**:
    - Click on the **Tune** button next to the **Simulation** button.
    - This opens the **tuning interface**, allowing real-time adjustments to circuit parameters.
    - Click the **Rstab** value under the .param section
2. **Fine-tune the inductor value**:
    - Adjust the **resistor size** while observing the **S11, S22, and K-factor**.

REMARK: As we have introduced a resistor that basically attenuates our bias we may need to increase the bias voltage. The reader is encouraged to explore different tuning parameters for bias, resistor value etc. Remember RF design is loop so getting the exact solution is nearly impossible :) Find your own sweat spot. 
