# test scikit-rf vector fit for S-parameters

import os
import skrf 
import argparse
from matplotlib import pyplot as plt
import numpy as np

print('Vector fitting from SnP S-parameter file')
print('Command line parameters: SnP_filename [numpoles]')
print('If numpoles parameter is not specified, it will be determined automatically!\n')


# evaluate commandline
parser = argparse.ArgumentParser()
parser.add_argument("snp",  help="SnP input filename (Touchstone format)")
parser.add_argument("numpoles",  help="Number of real poles (default=automatic)", default=0, nargs='?', type=int)
args = parser.parse_args()

# evaluate optional parameters
numpoles = args.numpoles 

# input data, must be n-port Touchstone data
nw = skrf.Network(args.snp)

# frequency class, see https://github.com/scikit-rf/scikit-rf/blob/master/skrf/frequency.py
freq = nw.frequency
f = freq.f

# vector fitting
vf = skrf.VectorFitting(nw)
if numpoles > 0:
  vf.vector_fit(n_poles_real=numpoles, n_poles_cmplx=0)
  fitmode = 'defined by commandline parameter'
else:  
  vf.auto_fit()
  fitmode = 'determined automatically'

# check if input data is passive
nw_is_passive  = nw.is_passive()

print('S-parameter frequency range is ',freq.start/1e9, ' to ', freq.stop/1e9, ' GHz')
print('Input S-parameter data is passive = ', nw_is_passive)
print(f'Model order used for fit = {vf.get_model_order(vf.poles)} {fitmode}')

# vf.plot_convergence()

# get fitting error
rms_error = vf.get_rms_error()
print('RMS error = ', rms_error)


fit_is_passive = vf.is_passive()
print('\nFitted data is passive = ', fit_is_passive)

# enforce passivity if required
if not fit_is_passive: # False: # not fit_is_passive:
  viol_bands = vf.passivity_test()
  print(f'Initial passivity violation bands = \n{viol_bands}')
  print(' Enforcing passivity for fitted data...')
  vf.passivity_enforce()
  fit_is_passive = vf.is_passive()
  print('Fitted data is passive now = ', fit_is_passive)
  

# get filename without extension
base_filename = os.path.splitext(args.snp)[0]
extension = os.path.splitext(args.snp)[1]

# write SPICE netlist
netlist_filename = base_filename + '.sp'
vf.write_spice_subcircuit_s(netlist_filename)


# write S-parameter file of fitted network
print('Creating  S-parameter file')
predicted_filename = base_filename + '_predicted' + extension
matrixsize = vf.network.nports
numfreq = 201
f_predicted = np.linspace(0, 2*freq.stop, numfreq)

snp_file = open(predicted_filename, 'w')
snp_file.write('#   Hz   S  RI   R   50\n')
snp_file.write('!\n')

# address elements as Sij
for index in range(0, numfreq):
  line = f"{f_predicted[index]:.6e}" 

  # multiport data
  for j in range(0,matrixsize):   
    for i in range(0,matrixsize):  
      Sij_fit = vf.get_model_response(i, j, [f_predicted[index]])
      line = line + f" {Sij_fit[0].real:.6e} {Sij_fit[0].imag:.6e}"

  snp_file.write(line + '\n')
snp_file.close()



# check data against fit over extended frequency range
freqs1 = np.linspace(0, 2*freq.stop, 201)
fig, ax = plt.subplots(2, 2)
fig.set_size_inches(12, 8)
vf.plot_s_mag(0, 0, freqs1, ax=ax[0][0]) # plot s11
vf.plot_s_mag(1, 0, freqs1, ax=ax[1][0]) # plot s21
vf.plot_s_mag(0, 1, freqs1, ax=ax[0][1]) # plot s12
vf.plot_s_mag(1, 1, freqs1, ax=ax[1][1]) # plot s22
fig.tight_layout()
plt.show()


