""" Module read_xyz
"""


def read_xyz(xyz_file):
    """ Module read_xyz

        Parameters
        ----------
        xyz_file : string
            Name of the xyz formatted filename (with path specified) to be read.

        Returns
        -------
        geom : list
            XYZ geometry stored in a list with each item specified as [atom_symbol, (x, y, z)]
    """

    geom = []
    with open(xyz_file,'r') as file1:

        for lc,lines in enumerate(file1):
            fields = lines.split()

            # Grab number of atoms
            if lc == 0:
                num_atoms = int(fields[0])

            # Grab geometry info
            if len(fields) == 4:
                # [atom,(x,y,z)]
                geom.append( [fields[0],(float(fields[1]),float(fields[2]),float(fields[3]))] )

    return(geom)
