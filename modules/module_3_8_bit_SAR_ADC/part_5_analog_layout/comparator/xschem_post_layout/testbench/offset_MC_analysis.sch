v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -540 -180 -540 -160 {
lab=vbias}
N -610 -180 -610 -160 {
lab=vdd}
N -610 -100 -610 -80 {
lab=GND}
N -570 -80 -540 -80 {
lab=GND}
N -420 -180 -420 -160 {
lab=clk}
N -420 -100 -420 -70 {
lab=GND}
N -570 -80 -570 -70 {
lab=GND}
N -420 -70 -210 -70 {
lab=GND}
N -210 -100 -210 -70 {
lab=GND}
N -210 -180 -210 -160 {
lab=vinp}
N 60 -220 120 -220 {
lab=vbias}
N 200 -120 200 -90 {
lab=GND}
N 250 -140 250 -110 {
lab=clk}
N 200 -350 200 -320 {
lab=vdd}
N 400 -210 500 -210 {
lab=outm}
N 400 -230 500 -230 {
lab=outp}
N 80 -160 120 -160 {
lab=vbias}
N 80 -280 120 -280 {
lab=vinp}
N -610 -80 -570 -80 {
lab=GND}
N -540 -100 -540 -80 {
lab=GND}
N 80 -300 80 -280 {
lab=vinp}
N 60 -280 80 -280 {
lab=vinp}
N 80 -160 80 -140 {
lab=vbias}
N 60 -160 80 -160 {
lab=vbias}
N 80 -80 80 -60 {
lab=GND}
N 80 -380 80 -360 {
lab=GND}
N 460 -150 460 -140 {
lab=GND}
N 460 -300 460 -290 {
lab=GND}
C {vsource.sym} -610 -130 0 0 {name=V3 value="DC 1.2"}
C {vsource.sym} -540 -130 0 0 {name=V4 value="DC 0.6"}
C {gnd.sym} -310 -70 0 0 {name=l1 lab=GND}
C {lab_pin.sym} -540 -180 2 0 {name=p3 sig_type=std_logic lab=vbias}
C {lab_pin.sym} -610 -180 2 0 {name=p4 sig_type=std_logic lab=vdd}
C {vsource.sym} -420 -130 0 0 {name=V1 value="PULSE(0 1.2 0 0 0 5N \{period\})"}
C {lab_pin.sym} -420 -180 2 0 {name=p1 sig_type=std_logic lab=clk}
C {gnd.sym} -570 -70 0 0 {name=l2 lab=GND}
C {vsource.sym} -210 -130 0 0 {name=V2 value="PULSE(595e-3 605e-3 0 tr 1S 1S)"}
C {lab_pin.sym} -210 -180 2 0 {name=p2 sig_type=std_logic lab=vinp}
C {lab_pin.sym} 60 -280 2 1 {name=p5 sig_type=std_logic lab=vinp}
C {lab_pin.sym} 200 -350 2 0 {name=p6 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 60 -220 2 1 {name=p7 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 60 -160 2 1 {name=p8 sig_type=std_logic lab=vbias}
C {lab_pin.sym} 250 -110 2 0 {name=p9 sig_type=std_logic lab=clk}
C {gnd.sym} 200 -90 0 0 {name=l3 lab=GND}
C {lab_pin.sym} 500 -230 2 0 {name=p10 sig_type=std_logic lab=outp}
C {lab_pin.sym} 500 -210 2 0 {name=p11 sig_type=std_logic lab=outm}
C {capa.sym} 80 -110 0 0 {name=C1
m=1
value=6.4p
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 80 -60 0 0 {name=l4 lab=GND}
C {gnd.sym} 80 -380 2 0 {name=l5 lab=GND}
C {capa.sym} 80 -330 2 0 {name=C2
m=1
value=6.4p
footprint=1206
device="ceramic capacitor"}
C {capa.sym} 460 -260 2 0 {name=C4
m=1
value=50f
footprint=1206
device="ceramic capacitor"}
C {capa.sym} 460 -180 0 0 {name=C3
m=1
value=50f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 460 -140 0 0 {name=l6 lab=GND}
C {gnd.sym} 460 -300 2 0 {name=l7 lab=GND}
C {devices/code_shown.sym} 15 -480 0 0 {name=MODEL1 only_toplevel=false
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt_mismatch
"}
C {devices/code_shown.sym} -675 -780 0 0 {name=NGSPICE1 only_toplevel=false 
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
    meas tran offset_voltage_\{$run\} find vindiff at=cross_time
    let results[$run - 1] = offset_voltage_\{$run\}
    let run = run + 1
  end
  print results > offset_MC_analysis.txt
  write offset_MC_analysis.raw
.endc

"}
C {dynamic_comparator.sym} 270 -220 0 0 {name=x1}
