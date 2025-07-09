class TransistorSweep:
    def __init__(self, mos_type, vgs, vds, vbs, length):
        """
        mos_type   : str ("nmos", "pmos")
        vgs        : tuple (start, stop, step) for gate-source voltage
        vds        : tuple (start, stop, step) for drain-source voltage
        vbs        : tuple (start, stop, step) for bulk-source voltage
        length     : list of channel lengths
        """
        self.mos_type = mos_type
        self.vgs = vgs
        self.vds = vds
        self.vbs = vbs
        self.length = length
