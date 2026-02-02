# Layout and Physical Verification

In this tutorial, we will guide you through the systematic process of laying out the bandgap reference circuit. This task is divided into two parts: the design of the two-stage OTA and the bandgap core, both of which were created in parts 1 and 2 of this series. The primary focus here is to transition the design from the schematic editor into KLayout for layout implementation, ensuring that pycells are correctly utilized in the layout process.

### Extracting Pycells from the Netlist and Performing LVS

Within part 3 of the tutorial, you will find the recommended setup for organizing your layout procedure. The `pycell_macro` folder contains the generator script we will use to create the layout. This script takes a netlist in the `.spice` format as input and processes it in batch mode. Here’s an example of how to use it for the two-stage OTA:

### Exporting the Netlist Correctly

Before starting the layout design, we must first export the netlist properly. To begin, launch the OTA design in **xschem** and navigate to the **Simulation** submenu. Within this menu, select the **LVS** option. Ensure that the **Use 'spiceprefix' attribute** checkbox is selected. Once this is done, click on **Netlist** to generate the corresponding simulation files.

Navigate to the simulation folder, which is located in the same directory as your schematic file. You should see a `.spice` file with the same name as the schematic. Open this file in your preferred text editor. The content will look like the following:

```
** sch_path: /home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_1_OTA/schematic/two_stage_OTA.sch
**.subckt two_stage_OTA vdd iout v+ v- vout vss
*.iopin v-
*.iopin v+
*.iopin vss
*.iopin vdd
*.iopin iout
*.iopin vout
XM4 net3 net1 vss vss sg13_lv_nmos w=720n l=9.75u ng=1 m=1
XM3 net1 net1 vss vss sg13_lv_nmos w=720n l=9.75u ng=1 m=1
XM1 net1 v- net2 vdd sg13_lv_pmos w=3.705u l=3.64u ng=1 m=1
XM2 net3 v+ net2 vdd sg13_lv_pmos w=3.705u l=3.64u ng=1 m=1
XM5 net2 iout vdd vdd sg13_lv_pmos w=5.3u l=1.95u ng=1 m=1
XM7 vout iout vdd vdd sg13_lv_pmos w=75u l=2.08u ng=8 m=1
XM6 vout net3 vss vss sg13_lv_nmos w=28.8u l=9.75u ng=4 m=1
XM9 iout iout vdd vdd sg13_lv_pmos w=75u l=2.08u ng=8 m=1
XC2 net3 vout cap_cmim w=22.295e-6 l=22.295e-6 m=1
**.ends
.end
```
### Understanding the Netlist

A netlist is essentially a list of components and their connections used for simulations. Here's a breakdown of the main elements:

- **Subcircuit Definition (`.subckt`)**: Defines the name of the circuit and its connections (e.g., `vdd`, `iout`, `v+`, etc.).
- **Device Definitions (`XM`, `XC`)**: These lines represent components (e.g., transistors and capacitors) and their connections, along with key parameters like width, length, and model.
- **Pins (`.iopin`)**: Specifies external connection points for the subcircuit.
- **End Markers (`.ends`, `.end`)**: Marks the beginning and end of the subcircuit and netlist.


### Creating the Device Gallery

With the netlist verified, we can now proceed to create the GDS file containing our layout. To achieve this, we will utilize the generator script located in the `pycell_macro` folder. We want to run it in batch mode. Here’s the general form for executing the script:

```
klayout -n sg13g2 -zz -r generator.py -rd netlist=netlist.spice -rd output=macros/gallery.gds
```

For my setup, the generator and netlist files are located as follows:

```
/home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_3_layout/pycell_macro/generator.py
```

```
/home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_1_OTA/schematic/simulations/two_stage_OTA.spice
```

The output file will be placed here:

```
/home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_3_layout/OTA_layout/two_stage_OTA.gds
```

Thus, the final command to generate the GDS file will be:

```
klayout -n sg13g2 -zz -r /home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_3_layout/pycell_macro/generator.py -rd netlist=/home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_1_OTA/schematic/simulations/two_stage_OTA.spice -rd output=/home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_3_layout/OTA_layout/two_stage_OTA.gds
```

After running this command, you can open the generated GDS file in KLayout using the following command:

```
klayout two_stage_OTA.gds -e
```
### Changing the Netlist Format for LVS

As we move into the layout phase, performing LVS (Layout vs. Schematic) checks is crucial to ensure that the layout matches the schematic design. Preparing the netlist in the correct format is a key step in this process. 

1. **Generate the Netlist in Xschem**:
    
    - Open your schematic in **Xschem**.
    - Navigate to the **Simulation** submenu and select the **LVS** option.
    - Deselect the **Use 'spiceprefix' attribute** checkbox.
    - Enable the option **LVS netlist: Top level is a .subckt**.
    - Click **Netlist** to generate the required file.

2. **Inspect the spice File**:
    
    - Open the `.spice` file in a text editor to ensure its contents look correct. You should see something like this:

```
** sch_path: /home/pedersen/projects/IHP-AnalogAcademy/modules/module_1_bandgap_reference/part_1_OTA/schematic/two_stage_OTA.sch
.subckt two_stage_OTA vdd iout v+ v- vout vss
*.PININFO v-:B v+:B vss:B vdd:B iout:B vout:B
M4 net3 net1 vss vss sg13_lv_nmos l=9.75u w=720n ng=1 m=1
M3 net1 net1 vss vss sg13_lv_nmos l=9.75u w=720n ng=1 m=1
M1 net1 v- net2 vdd sg13_lv_pmos l=3.64u w=3.705u ng=1 m=1
M2 net3 v+ net2 vdd sg13_lv_pmos l=3.64u w=3.705u ng=1 m=1
M5 net2 iout vdd vdd sg13_lv_pmos l=1.95u w=5.3u ng=1 m=1
M7 vout iout vdd vdd sg13_lv_pmos l=2.08u w=75u ng=8 m=1
M6 vout net3 vss vss sg13_lv_nmos l=9.75u w=28.8u ng=4 m=1
M9 iout iout vdd vdd sg13_lv_pmos l=2.08u w=75u ng=8 m=1
C2 net3 vout cap_cmim w=22.295e-6 l=22.295e-6 m=1
.ends
.end

```
- Note that the instance prefixes (e.g., `X`) have been removed, which is necessary for LVS.
    
- **Update the Layout in KLayout**:
    
    - Open the layout in **KLayout**.
    - Navigate to the **Cells** menu and rename the top cell (e.g., `gallery`) to match the top cell name in your netlist. For instance, rename it to `two_stage_OTA` in this case.
- **Run the LVS in KLayout**:
    
    - Open the **SG13G2 PDK** menu and select **SG13G2 LVS Options**.
    - In the small menu that appears, specify the path to your `.spice` netlist file (remeber to select .spice as file format).
    - Click **OK** to save the settings.
    - Finally, navigate to the **LVS** option in the same menu to run the LVS check.


At this point you should see a lot of uncorrected LVS issues.


# Klayout video tutorial
The linked video provides a walkthrough on designing the input pair of an OTA for a bandgap reference and demonstrates how to complete a layout using open-source tools. While this is not a comprehensive, 
end-to-end tutorial—such a deep dive would require far more time than is practical for a single video—it covers the essentials.
You’ll learn how to navigate KLayout effectively and establish a solid layout workflow, laying the foundation for more advanced design tasks.

Link to layout tutorial:
https://youtu.be/tOYrJKtNuaw
