import numpy as np

bsize_sp = 512
mdata_list = [
    b"title",
    b"date",
    b"plotname",
    b"flags",
    b"no. variables",
    b"no. points",
    b"dimensions",
    b"command",
    b"option",
]

def parse_file(fname):
    """
    Read ngspice binary raw files. Return tuple of the data, and the
    plot metadata. The dtype of the data contains field names.
    """
    with open(fname, "rb") as fp:
        plot = {}
        arrs = []
        plots = []
        while True:
            mdata = fp.readline(bsize_sp).split(b":", maxsplit=1)
            if len(mdata) == 2:
                key = mdata[0].lower()
                if key in mdata_list:
                    plot[key] = mdata[1].strip()
                elif key == b"variables":
                    nvars = int(plot[b"no. variables"])
                    npoints = int(plot[b"no. points"])
                    varspecs = [
                        fp.readline(bsize_sp).strip().decode("ascii").split()
                        for _ in range(nvars)
                    ]
                    plot["varnames"], plot["varunits"] = zip(
                        *[(spec[1], spec[2]) for spec in varspecs]
                    )
                elif key == b"binary":
                    rowdtype = np.dtype(
                        {
                            "names": plot["varnames"],
                            "formats": [
                                np.complex128
                                if b"complex" in plot[b"flags"]
                                else np.float64
                            ]
                            * nvars,
                        }
                    )
                    arrs.append(np.fromfile(fp, dtype=rowdtype, count=npoints))
                    plots.append(plot.copy())
                    fp.readline()
            else:
                break
    return (arrs, plots)

