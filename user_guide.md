# 📘 Analog Academy – User Guide

Welcome to the **IHP Analog Certificate Course**, part of the publicly funded FMD-QNC project (16ME083) by the **Federal Ministry of Research, Technology and Space (BMFTR)**.  
More info: [FMD-QNC Project Website](https://www.elektronikforschung.de/projekte/fmd-qnc)

---

## 🧭 How to Use This Course

This course provides a hands-on introduction to analog, RF, and mixed-signal IC design using **open-source tools** and the **IHP Open PDK (SG13G2 130nm technology)**.

> ⚠️ **Note:** This is *not* a beginner's IC design course. A basic understanding of electronics and microelectronics is required.

---

## 📂 Navigating the Repository

- **Go to the `modules/` folder**  
  Start with the module's `README.md`, then follow the numbered `part_*` folders for the hands-on tutorial.

- **Use the `slides/` folder for reference only**  
  These are PowerPoint slides from the in-person course at IHP.  
  They’re *not* intended to be followed alone for self-study, as some content was delivered live and may lack context.

---

## 🧱 Course Modules

| Module | Topic                             |
|--------|-----------------------------------|
| 0      | Foundations (tools + gm/Id flow)  |
| 1      | Bandgap Reference                 |
| 2      | 50GHz Medium Power Amplifier      |
| 3      | 8-bit SAR ADC                     |
| 4      | [StrongARM Latch Design](modules/module_4_strong_arm_latch/README.md) – 1 or 2 days |

Modules 0–3 form the original course sequence, combining theory with practical exercises. **Module 4 is a standalone workshop that can be delivered in 1 or 2 days depending on the audience's level:** one day for experienced participants, or two days for participants who need more guided practice with the design flow. It requires the tool setup from Module 0 and basic electronics knowledge.

## Getting the StrongARM Latch Design

The actual design is included in `modules/module_4_strong_arm_latch/IHP__CMP7345` as a Git submodule of [KrzysztofHerman/IHP__CMP7345](https://github.com/KrzysztofHerman/IHP__CMP7345).

From an existing academy checkout, run:

```bash
git submodule update --init --recursive
```

For a new checkout, use:

```bash
git clone --recurse-submodules https://github.com/KrzysztofHerman/IHP-AnalogAcademy.git
```

Follow the [Module 4 setup and schedule](modules/module_4_strong_arm_latch/README.md) before opening its schematics. The [StrongARM workshop slides](slides/StrongARM_Latch/README.md) complement the written exercises.
