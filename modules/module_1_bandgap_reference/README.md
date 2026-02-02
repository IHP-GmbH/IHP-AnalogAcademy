# Bandgap design

In integrated circuit (IC) design many circuits require a fixed stable, temperature independent voltage fixation in order to have a constant voltage reference.
The use case for these stable references, could be used to provide a stable reference to data converters or bias operating points. These circuits is also called Bandgap References or in short BGR. 
They work by summing a proportional to absolute temperature device with a complementary proportional to absolute temperature device together, or in other words: The bandgap reference is comprised of two 
devices with opposite temperature coefficients within a given interval of interest.

 One of devices that exhibits inherent negative TC s is the bipolar junction transistor (BJT). The relation of the base to emitter voltage can be described with the following equation given as:

$$V_{BE} = V_T \cdot ln(\frac{I_C}{I_S})$$

Where $I_C$ is the collector current and $I_S$ is the saturation current. 
The theory behind different circuit topology regarding the bandgap references are quite comprehensive, and will therefore not be covered here. Instead the circuit seen below is proposed:

<p align="center"> <img src=".media/bandgap_circuit.png" width="800" height="700" /> </p>


From the following criteria, $I_{C,Q1}=I_{C,Q2}$ if $R_2 = R_3$, we can try to understand the circuit functionality. The voltage X and Y is forced to be equal due to the operation of the feedback of the OP-amps. This means that we can write the following expression

$$\vert V_{BE1}\vert = \vert V_{BE2}\vert + I_{C2}\cdot R_1$$
Making a simple KCL at node Y, shows that the current through $R_1$ must be given as

$$I_{C2} = \frac{\vert V_{BE1} \vert - \vert V_{BE2} \vert }{R_1}$$

$$I_{C2} = \frac{\left\vert V_T \cdot ln(\frac{I_{C1}}{I_{S1}})-V_T \cdot ln(n\cdot \frac{I_{C2}}{I_{S2}})\right\vert}{R_1}$$

Now we know that $I_{C1} = I_{C2}$ , and $I_{S1} = I_{S2}$ . This gives the following expression for $I_{C2}$

$$I_{C2} = \frac{V_T \cdot ln(n)}{R_1}$$
Now we see we can describe the whole current in the branch of M4 as 

$$I_{D4} = \frac{\vert V_{BE1}\vert}{R_2} + \frac{V_T \cdot ln (n)}{R_1}$$

In order to then set the bandgap voltage, the current is then copied out to the branch with the resistor $R_4$ and the relation can then be described by

$$V_{out} = I_{D4} \cdot R_4 = \frac{R_4}{R_2} \cdot \left(\vert V_{BE1}\vert + \frac{R_2}{R_1} V_T \cdot ln(n)\right) $$

So to  sum up the operation we see that the bandgap voltage is given as a upscaling of the PTAT of the BJT given by the ratio of discrete resistors. Without this upscaling the sizes of the BJT would be incredibly large and low voltage reference wouldn't be possible. We highly recommend the reader to dive into the theory behind this literature, specified in the bibliography of this chapter

# Bibliography

 - B. Razavi,“Design of Analog CMOS Integrated Circuits,” McGrawHill, second edition, Chapter 12
 - Ali Hajimiri lectures: https://www.youtube.com/watch?v=AMgrGvzCTck
