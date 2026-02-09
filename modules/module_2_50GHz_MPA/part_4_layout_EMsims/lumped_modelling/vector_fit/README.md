# vectorfit_sparam

This script reads n-port S-parameter data (*.snp) and calculates 
a wide band circuit model fit, using scikit-rf vector fit functionality.

Vector fit is done for each branch of the n-port data, with model fit order determined automatically. As an option, the user can also specify the model fit order on the command line. If no value is
specified, the required fit order will be determined automatically.

<img src="./doc/vectorfit.png" alt="vectorfit" width="700">



# Prerequisites
The code requires Python3 with the skitkit-rf library.
https://scikit-rf.readthedocs.io/en/latest/tutorials/index.html

# Usage
To run the vector fit, specify the *.snp file as the first parameter.  If no value for model order is
specified, the fit order will be determined automatically.

example:
```
(palace) C:\Users\volker\Downloads>D:\venv\palace\Scripts\python.exe d:\batch\vectorfit_sparam.py inductor3.s2p
Vector fitting from SnP S-parameter file
Command line parameters: SnP_filename [numpoles]
If numpoles parameter is not specified, it will be determined automatically!

S-parameter frequency range is  0.0  to  10.0  GHz
Input S-parameter data is passive =  True
Model order used for fit = 7 determined automatically
RMS error =  0.0007246029585921373

Fitted data is passive =  True
Creating  S-parameter file
```

The result of the fit is stored in netlist format.


# Accuracy
You can see from the plot if the model fits well. As an additional check, 
an S-parameter output file with suffix ".predicted" is created, which
correspondonds to the fitted model. This can be used to verify the fit 
against input data.

<img src="./doc/netlist_output.png" alt="netlist" width="500">
