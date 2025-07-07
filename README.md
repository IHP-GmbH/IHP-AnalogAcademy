<p align="center">
  <img src="media/ihp-logo.jpg"  width="600" height="400" />
</p>

The Development of this course is funded by the public german project FMD-QNC (16ME083) from BMFTR (Federal Ministry of Research, Technology and Space / Bundesministerium für Forschung, Technologie und Raumfahrt):
https://www.elektronikforschung.de/projekte/fmd-qnc

# Welcome to the IHP Analog Certificate Course

This course is designed to guide you through the world of analog, mixed-signal, and RF design using open-source tools and the IHP Open PDK, tailored for the 130nm technology node. The goal is to provide a practical understanding of analog workflows, from the basics to advanced techniques such as EM simulations, mixed-signal analysis, and Monte Carlo scripting.

**Please note**: This course is not an introduction to IC design. It assumes that you have a basic understanding of electronics and microelectronics. If you are unfamiliar with these topics, you may need supplementary resources to build foundational knowledge in these areas. This course is physically conducted at IHP, and while the workflow and procedures are outlined in this markdown, the course content is best understood in conjunction with the slides provided.

### Course Structure

The course is divided into several modules, each designed to build upon the previous one. Each module primarily emphasizes hands-on exercises and practical applications, with brief theory sections to support your learning.

For a structured learning experience, we encourage you to follow the **slides folder** in the repository to see the course outline and the schedule for the 5-day tutorial week. The slides can be used as the primary tutorial, but keep in mind that some parts were presented live, and you may need to refer to the markdown files for additional details..


## Table of contents
- [Introduction to IHP Open PDK and SG13G2 Technology](#introduction-to-ihp-open-pdk-and-sg13g2-technology)
- [Foundations](#module-0--foundations)
- [Bandgap Reference](#module-1--bandgap-reference)
- [50GHz Medium Power Amplifier](#module-2--50ghz-medium-power-amplifier)
- [8-bit SAR ADC](#module-3--8-bit-sar-adc)
- [Final Thoughts](#final-thoughts)



## Introduction to IHP Open PDK and SG13G2 Technology

### What is the IHP Open PDK?

The **IHP Open Source PDK** is a freely available Process Design Kit targeted at the **SG13G2 node**—a part of IHP’s 130nm SiGe BiCMOS process line. This PDK allows academic, research, and open-hardware communities to design **analog, digital, mixed-signal, and RF integrated circuits** using real-world manufacturing technology.

The IHP Open PDK includes the following:

- **Primitive and standard cell libraries**
    
- **Layout and DRC rules for KLayout**
    
- **Device models for simulation** (ngspice/Xyce)
    
- **Design examples and testbenches**
    
- **Documentation** including process specs and layout rules
    

> ⚠️ **Important**: The IHP Open PDK is currently in _preview status_ and is not yet qualified for production use. However, it serves as an ideal tool for educational and research purposes​.

### SG13G2 Technology Highlights

The **SG13G2 process** offers a wide range of advanced features:

- **0.13 µm CMOS technology** for efficient fabrication
    
- High-speed **SiGe:C NPN HBTs** with:
    
    - Up to **350 GHz** transition frequency (_fT_)
        
    - Up to **500 GHz** maximum oscillation frequency (_fmax_)
        
- **Dual gate oxides** for versatile applications:
    
    - Thin oxide for **1.2 V logic**
        
    - Thick oxide for **3.3 V I/O**
        
- Comprehensive device portfolio including:
    
    - **NMOS, PMOS, iNMOS, and HV devices**
        
    - **Poly resistors** (Rsil, Rppd), **MIM capacitors**
        
    - **5 thin and 2 thick Al metal layers** for routing
        
- Designed for **high-frequency** and **high-performance applications**
    

For further information, please visit the following sources:

- 🌐 [IHP Website](https://www.ihp-microelectronics.com/)
- 🏠 [IHP Open PDK Repository](https://github.com/IHP-GmbH/IHP-Open-PDK)
- 📚 [IHP Open PDK Docs](https://ihp-open-pdk-docs.readthedocs.io/en/latest/)
- 💬 [IHP Open PDK Discussion on ChatGPT](https://chatgpt.com/g/g-sovooLd0V-ihp-open-pdk)



## Module 0 – Foundations

This introductory module sets up the essential tools and methodologies for working with the IHP Open PDK in analog IC design. You'll begin by installing and verifying key tools like Xschem and KLayout, guided by the official documentation. Once installed, you’ll explore basic simulations—including DC, transient, AC, Monte Carlo, and S-parameter analyses—through example test cases provided within the PDK.

A modern design flow is introduced, emphasizing the **gm/Id methodology**, which replaces traditional square-law models with a more robust, data-driven approach. The course provides optional tools and scripts to generate and visualize gm/Id lookup tables compatible with the IHP PDK, laying the groundwork for advanced circuit design in later modules.

Whether you're new to IC design or transitioning to an open-source flow, this module ensures your environment is fully prepared for hands-on analog development using the IHP 130nm technology node.




## Module 1 – Bandgap Reference

In this module, you'll begin your first analog design: an all-CMOS bandgap reference. The module is divided into three parts, guiding you from OTA design to full schematic simulation and layout considerations.

---

### 🔧 Part 1 – Designing the OTA

We begin by designing the **operational transconductance amplifier (OTA)** used in the bandgap reference. A Jupyter Notebook with the `gm/Id` procedure is provided to assist in device sizing. While this procedure isn’t covered in depth, it serves as a helpful tool for those interested in data-driven transistor selection.

The focus of this stage is on the **AC performance** of the OTA. You’ll learn how to:

- Create a symbol for the OTA in **Xschem**,
    
- Simulate the design using **Ngspice**,
    
- And analyze the amplifier’s AC performance
    

---

### ⚙️ Part 2 – Building the Bandgap Reference

Next, you'll construct the full **bandgap reference schematic**. Here, you’ll start making practical design choices with eventual fabrication in mind.

This section covers:

- **DC and transient analysis** of the reference voltage,
    
- Considerations for component selection (e.g., resistors, transistor sizing),
    
- Incorporating **mismatch parameters** into your simulation models,
    
- Running your first **Monte Carlo analysis** to assess mismatch effects.
    

---

### 🧱 Part 3 – Layout Introduction

Finally, we introduce the **layout flow** using **KLayout**. A video guide is available to demonstrate the **common-centroid layout** technique for the OTA's input pair.

Although the complete layout of the bandgap reference isn’t covered step-by-step (as it's relatively straightforward), the **final layout is provided** for reference.

> 📌 **Note**: Be sure to consult both the slides and the Markdown file for this module. The slides include additional insights and layout screenshots not shown in the Markdown notes.






## Module 2 – 50 GHz Medium Power Amplifier

In this module, we take our first steps into the world of **RF design** by developing a **50 GHz Medium Power Amplifier (MPA)** using **QUCS-S** as the schematic editor.

---

### 🧪 Part 1 – Biasing & Familiarization with QUCS-S

We begin with the **biasing of a single-transistor amplifier**, a fundamental step in RF amplifier design. This part also serves as an introduction to **QUCS-S**, helping you get comfortable with its interface and simulation flow.

---

### 🎯 Part 2 – Input Matching with Smith Chart

Next, we tackle **input matching**, an essential part of ensuring power transfer and minimizing reflections. In QUCS-S, you’ll:

- Explore the **Smith chart** in Qucs-s,
    
- Use **tuner sliders** to adjust matching elements interactively,
    
- Generally plot relevant information
    


---

### 📈 Part 3 – Nonlinear Simulations with Xyce

Linear analysis is only part of the story—**nonlinear behavior** is critical for power amplifiers. Since **Ngspice currently lacks nonlinear support**, we shift to the **Xyce** simulator.

In this section:

- You’ll learn how to **run nonlinear simulations** using Xyce,
    
- Deal with some OS-related setup challenges,
    
- Perform **Python-based post-processing** of simulation data (scripts are provided).
    

This part introduces a more **realistic and complete RF design flow**, where we will look at how to extract key performance aspects. 

---

### 📡 Part 4 – EM Simulation with OpenEMS

The final section covers **electromagnetic (EM) simulation** of custom components, which is crucial when designing circuits at these frequencies.

Highlights include:

- Performing **3D EM simulations** with **OpenEMS** on a BJT core design,
    
- Using the **Python-based interface** developed specifically for the IHP process stack,
    
- Extracting **S-parameter files** from the EM simulation for use in schematic-level simulation.
    

This part showcases the **iterative nature of RF design**, where component models are refined through EM simulations.

> 📌 **Note**: Be sure to consult the slides for this module. It includes additional resources from the developer of the Python–OpenEMS interface for the IHP stackup, not covered in the Markdown file.





## Module 3 – 8-bit SAR ADC

In the final module, we shift focus to **mixed-signal design** by building a simple yet functional **8-bit Successive Approximation Register (SAR) ADC**. The chosen architecture is a **synchronous SAR**. 

---

### ⚙️ Part 1 – Dynamic Comparator Design & Analysis

We begin by designing the **dynamic comparator**, a crucial component of the ADC. The selected topology offers:

- **Low common-mode sensitivity**
    
- **Relatively low offset voltage**
    

In this section, we analyze the comparator through **transient simulations**, followed by an extended **Monte Carlo simulation** to estimate its offset behavior. You’ll learn how to:

- Set up parameter sweeps and statistical variations
    
- Write equations for automatic **offset extraction**
    
- Visualize results using a **Python script** to generate a histogram of Monte Carlo outcomes
    

---

### 🧩 Part 2 – Auxiliary Circuit Blocks

Next, we design and simulate some of the **supporting blocks** required for the ADC, such as:

- **Bootstrapped switches**
    
- **Transmission gates**
    
- **Inverters**
    

This part focuses on verifying the **basic functionality** of each block, which are essential building elements in the final system.

---

### 🔁 Part 3 – SAR Logic and Mixed-Signal Integration

With the analog blocks in place, we introduce the **SAR algorithm** and integrate it into a **mixed-signal simulation environment**. This part marks the first hands-on exposure to **co-simulation of analog and digital** behavior.

---

### 🧪 Part 4 – Final ADC Testbench and Output Analysis

The final part brings everything together:

- The **complete SAR ADC circuit** is assembled
    
- A **testbench** is built to verify the digital output
    
- A **Jupyter Lab notebook** is provided to post-process the output and reconstruct the analog input using an **ideal DAC model**
    

This section offers a clear view of the **end-to-end data conversion**.

> 📌 Be sure to explore both the Markdown and the accompanying slides for this module. Some additional insights and visualizations are included in the slides that aren’t covered in the Markdown material.





## Final Thoughts

This course emphasizes **key steps in the workflow** for analog, RF, and mixed-signal IC design using open-source tools. While we haven't covered every detail in depth, the aim was to provide a **strong foundation** for navigating the complexities of these workflows. We hope this serves as a good starting point, and that you'll take what you've learned here to explore further on your own.

Remember, this is just the beginning! We encourage you to experiment, adapt, and build upon the provided resources to strengthen your individual workflow.

We're also very open to feedback—whether it's pointing out errors, suggesting improvements, or sharing additional insights. Please feel free to submit any issues or ideas through the **Issues tab**.

Thanks for following along, and happy designing! 🚀

Current Commit of IHP-Open-PDK to work with the course: eb1b540c58346cf6259285a38d09b2a04feb344a
<<<<<<< HEAD


<p align="center">
  <img src="media/bmftr_en.jpg"  width="300" height="200" />
</p>
=======
>>>>>>> 40e222618b8bb24df992a297feef0bac8f871dd0
