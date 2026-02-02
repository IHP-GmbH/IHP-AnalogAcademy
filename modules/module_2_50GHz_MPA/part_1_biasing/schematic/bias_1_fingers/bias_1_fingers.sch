<Qucs Schematic 25.1.2>
<Properties>
  <View=827,-128,2728,609,1.59023,0,0>
  <Grid=10,10,1>
  <DataSet=bias_1_fingers.dat>
  <DataDisplay=bias_1_fingers.dpl>
  <OpenDisplay=0>
  <Script=bias_1_fingers_for_course.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <DCBlock C11 1 1520 270 -26 21 0 0 "1 uF" 0>
  <DCFeed L5 1 1600 320 20 -26 0 1 "1 uH" 0>
  <DCFeed L8 1 1780 50 20 -26 0 1 "1 uH" 0>
  <IProbe Pr1 1 1780 160 18 -26 1 3>
  <Vdc V3 1 1600 410 18 -26 0 1 "0.97 V" 1>
  <GND * 1 1360 450 0 0 0 0>
  <GND * 1 1600 440 0 0 0 0>
  <GND * 1 1820 270 0 0 0 0>
  <DCBlock C12 1 1990 100 -26 21 0 0 "1 uF" 0>
  <GND * 1 2120 170 0 0 0 0>
  <GND * 1 1960 380 0 0 0 0>
  <Vdc V1 1 1960 330 18 -26 0 1 "1.65V" 1>
  <INCLSCR INCLSCR2 1 1420 180 -60 16 0 0 ".LIB cornerHBT.lib hbt_typ\n" 1 "" 0 "" 0>
  <.DC DC1 1 1530 20 0 36 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <GND * 1 1780 450 0 0 0 0>
  <Pac P3 1 1360 370 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "50 GHz" 0 "26.85" 0 "true" 0>
  <Pac P4 1 2120 140 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "50 GHz" 0 "26.85" 0 "true" 0>
  <NutmegEq NutmegEq1 1 1380 540 -28 16 0 0 "SP1" 1 "k=(1 - abs(s_1_1)^2 - abs(s_2_2)^2 + abs(s_1_1 * s_2_2 - s_1_2 * s_2_1)^2) / (2 * abs(s_1_2 * s_2_1))\n" 1>
  <.SP SP1 1 1360 10 0 61 0 0 "lin" 1 "1 GHz" 1 "200 GHz" 1 "200" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Lib npn13G3 1 1780 270 10 64 0 0 "/home/pedersen/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "npn13G2" 0 "10" 1>
</Components>
<Wires>
  <1360 270 1490 270 "" 0 0 0 "">
  <1360 270 1360 340 "" 0 0 0 "">
  <1550 270 1600 270 "" 0 0 0 "">
  <1600 270 1750 270 "" 0 0 0 "">
  <1600 270 1600 290 "" 0 0 0 "">
  <1600 350 1600 380 "" 0 0 0 "">
  <1780 80 1780 100 "" 0 0 0 "">
  <1780 100 1780 130 "" 0 0 0 "">
  <1780 190 1780 220 "Collector_voltage" 1810 170 14 "">
  <1360 400 1360 450 "" 0 0 0 "">
  <1790 270 1820 270 "" 0 0 0 "">
  <1780 -20 1780 20 "" 0 0 0 "">
  <1780 100 1960 100 "" 0 0 0 "">
  <2020 100 2120 100 "" 0 0 0 "">
  <2120 100 2120 110 "" 0 0 0 "">
  <1960 360 1960 380 "" 0 0 0 "">
  <1960 270 1960 300 "" 0 0 0 "">
  <1780 320 1780 450 "" 0 0 0 "">
  <1780 -20 1780 -20 "Vcc" 1810 -50 0 "">
  <1960 270 1960 270 "Vcc" 1990 240 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
