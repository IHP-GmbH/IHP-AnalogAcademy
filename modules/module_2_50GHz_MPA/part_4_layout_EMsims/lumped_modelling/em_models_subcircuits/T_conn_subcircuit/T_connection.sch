<Qucs Schematic 25.1.2>
<Properties>
  <View=423,218,804,501,1.6378,0,0>
  <Grid=10,10,1>
  <DataSet=T_connection.dat>
  <DataDisplay=T_connection.dpl>
  <OpenDisplay=0>
  <Script=T_connection.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID 30 14 SUB>
  <.PortSym -110 -20 1 0 P1>
  <.PortSym 110 -20 2 180 P2>
  <.PortSym 0 70 3 90 P3>
  <Line -110 -20 10 0 #000080 2 1>
  <Line 100 -20 10 0 #000080 2 1>
  <Line 0 70 0 -10 #000080 2 1>
  <Line -100 -30 120 0 #000080 2 1>
  <Line 100 -30 0 30 #000080 2 1>
  <Line -100 -30 0 30 #000080 2 1>
  <Line 20 -30 80 0 #000080 2 1>
  <Line -100 0 80 0 #000080 2 1>
  <Line -20 0 0 30 #000080 2 1>
  <Line 20 0 0 30 #000080 2 1>
  <Line 20 0 80 0 #000080 2 1>
  <Line -20 30 0 30 #000080 2 1>
  <Line 20 30 0 30 #000080 2 1>
  <Line -20 60 40 0 #000080 2 1>
</Symbol>
<Components>
  <GND * 1 600 420 0 0 0 0>
  <Port P1 1 490 330 -23 12 0 0 "1" 1 "analog" 0>
  <Port P3 1 490 390 -23 12 0 0 "3" 1 "analog" 0>
  <Port P2 1 710 330 4 -46 0 2 "2" 1 "analog" 0>
  <SPICE T_connection 1 600 360 -26 -85 0 0 "../../../em_components/T_connection_2/openems/output/run_t_con_50GHZ_data/run_t_con_50GHZ.sp" 0 "_netp1,_netp2,_netp3" 0 "yes" 0 "none" 0 "" 0>
</Components>
<Wires>
  <490 330 570 330 "" 0 0 0 "">
  <490 390 570 390 "" 0 0 0 "">
  <630 330 710 330 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
