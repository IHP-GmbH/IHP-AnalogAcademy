<Qucs Schematic 25.1.2>
<Properties>
  <View=383,241,824,569,1.41497,0,0>
  <Grid=10,10,1>
  <DataSet=BJT_core.dat>
  <DataDisplay=BJT_core.dpl>
  <OpenDisplay=0>
  <Script=BJT_core.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID 50 -106 SUB>
  <.PortSym 70 0 2 180 Port_2>
  <.PortSym -30 80 3 90 Port_3>
  <.PortSym 30 80 4 90 Port_4>
  <.PortSym -60 0 1 0 Port_1>
  <Line 70 0 -10 0 #000080 2 1>
  <Line -30 70 0 10 #000080 2 1>
  <Line 30 80 0 -10 #000080 2 1>
  <Line -50 0 -10 0 #000080 2 1>
  <Line -50 -70 110 0 #000080 2 1>
  <Line -50 -10 0 30 #000000 1 1>
  <Line -20 70 40 0 #000000 1 1>
  <Line 60 -10 0 30 #000000 1 1>
  <Line 60 -70 0 140 #000080 2 1>
  <Line -50 70 110 0 #000080 2 1>
  <Line -50 -70 0 140 #000080 2 1>
  <Line -40 0 20 0 #000000 1 1>
  <Line -20 0 20 -20 #000000 1 1>
  <Line -40 10 20 0 #000000 1 1>
  <Line -20 10 20 20 #000000 1 1>
  <Line 0 -20 0 50 #000000 1 1>
  <Line 0 30 10 0 #000000 1 1>
  <Line 10 -20 0 50 #000000 1 1>
  <Line 0 -20 10 0 #000000 1 1>
  <Line 10 -20 20 20 #000000 1 1>
  <Line 30 0 20 0 #000000 1 1>
  <Line 30 10 20 0 #000000 1 1>
  <Line 30 10 -20 20 #000000 1 1>
  <Rectangle 0 -30 10 70 #000000 1 1 #c0c0c0 1 1>
</Symbol>
<Components>
  <GND * 1 580 490 0 0 0 0>
  <Port Port_1 1 450 350 -23 12 0 0 "1" 1 "analog" 0>
  <Port Port_3 1 450 410 -23 12 0 0 "3" 1 "analog" 0>
  <Port Port_2 1 730 350 4 12 1 2 "2" 1 "analog" 0>
  <Port Port_4 1 730 410 4 12 1 2 "4" 1 "analog" 0>
  <SPICE BJT_Core 1 580 380 -26 -85 0 0 "../../../em_components/core_1/openems/output/run_core_50ghz_mpa_data/run_core_50ghz_mpa.sp" 0 "_netp1,_netp2,_netp3,_netp4" 0 "yes" 0 "none" 0 "" 0>
</Components>
<Wires>
  <450 350 550 350 "" 0 0 0 "">
  <610 350 730 350 "" 0 0 0 "">
  <450 410 550 410 "" 0 0 0 "">
  <610 410 730 410 "" 0 0 0 "">
  <580 440 580 490 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
