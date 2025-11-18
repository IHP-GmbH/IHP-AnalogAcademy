# LC VCO

- Description: LC based voltage controlled oscillator
- PDK: ihp-sg13g2

## Authorship

- Designer: Phillip F. Baade-Pedersen
- Company: IHP
- Created: None
- License: Apache 2.0
- Last modified: None

## Pins

- VDD
  + Description: Positive analog power supply
  + Type: power
  + Direction: inout
  + Vmin: 0.8
  + Vmax: 1.6
- Vinplus
  + Description: Positive Input
  + Type: signal
  + Direction: input
- Vinminus
  + Description: Negative Input
  + Type: signal
  + Direction: input

## Default Conditions

- vdd
  + Description: Analog power supply voltage
  + Display: Vdd
  + Unit: V
  + Typical: 1.2
- corner
  + Description: Process corner
  + Display: Corner
  + Typical: tt
- temperature
  + Description: Ambient temperature
  + Display: Temp
  + Unit: °C
  + Typical: 27

## Symbol

![Symbol of LC VCO](LC VCO_symbol.svg)

## Schematic

![Schematic of LC VCO](LC VCO_schematic.svg)
