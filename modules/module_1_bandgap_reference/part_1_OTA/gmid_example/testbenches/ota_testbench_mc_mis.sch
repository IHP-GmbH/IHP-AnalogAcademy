v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 725 -405 725 -375 {
lab=vp}
N 960 -405 960 -375 {
lab=vdd}
N 960 -315 960 -295 {
lab=GND}
N 835 -295 960 -295 {
lab=GND}
N 295 -485 295 -465 {
lab=GND}
N 295 -630 295 -615 {
lab=vdd}
N 140 -590 160 -590 {
lab=vp}
N 140 -505 160 -505 {
lab=vout}
N 480 -490 480 -475 {
lab=GND}
N 160 -505 160 -250 {
lab=vout}
N 835 -295 835 -275 {
lab=GND}
N 725 -295 835 -295 {
lab=GND}
N 725 -315 725 -295 {
lab=GND}
N 540 -550 570 -550 {
lab=vout}
N 540 -550 540 -250 {
lab=vout}
N 460 -550 540 -550 {
lab=vout}
N 220 -465 220 -430 {
lab=#net1}
N 220 -370 220 -355 {
lab=GND}
N 160 -250 540 -250 {
lab=vout}
C {vsource.sym} 725 -345 0 0 {name=V1 value="DC 0.6 AC 1 0"
}
C {vsource.sym} 960 -345 0 0 {name=VDD value="DC 1.2"}
C {gnd.sym} 835 -275 0 0 {name=l1 lab=GND}
C {gnd.sym} 295 -465 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 295 -630 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 960 -405 0 0 {name=p2 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 725 -405 0 0 {name=p3 sig_type=std_logic lab=vp}
C {lab_pin.sym} 140 -590 0 0 {name=p5 sig_type=std_logic lab=vp}
C {isource.sym} 220 -400 0 0 {name=I0 value=80u}
C {gnd.sym} 220 -355 0 0 {name=l3 lab=GND}
C {capa.sym} 480 -520 0 0 {name=Cload
m=1
value=500f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 480 -475 0 0 {name=l5 lab=GND}
C {iopin.sym} 570 -550 0 0 {name=p7 lab=vout}
C {devices/code_shown.sym} 95 -770 0 0 {name=MODEL only_toplevel=false
format="tcleval( @value )"
value="
.lib cornerCAP.lib cap_typ
.lib cornerMOSlv.lib mos_tt_mismatch
"}
C {devices/code_shown.sym} 25 -1260 0 0 {name=NGSPICE only_toplevel=false 
value="
.control
  let run = 1
  let mc_runs = 100
  set curplot = new
  set scratch = $curplot
  dowhile run <= mc_runs
    reset
    dc temp 0 70 5
    set run = $&run
    set dc = $curplot
    setplot $scratch
    let off\{$run\} = \{$dc\}.v(vout)
    let mytemp\{$run\} = \\"\{$dc\}.temp-sweep\\"
    setplot $dc
    let run = run + 1
  end
  set nolegend
  plot \{$scratch\}.allv vs \{$scratch\}.mytemp1
  write ota_testbench_mc_mis.raw \{$scratch\}.allv \{$scratch\}.mytemp1
.endc

"}
C {launcher.sym} 430 -635 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/output_file.raw ac"
}
C {two_stage_OTA.sym} 310 -550 0 0 {name=x1}
