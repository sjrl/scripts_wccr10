"""Module input_utils

This module contains useful utility functions that are general for writing Molpro input files.
"""

# Function to write a basis set to an open file
def writeBasis(out_file,basis,
               rpa=False,mixed=False):
    if rpa:
        out_file.write('basis={\n')
        out_file.write('set,orbital\n')
        out_file.write('default,{:s}\n'.format(basis))
        out_file.write('set,mp2fit\n')
        out_file.write('default,{:s}/mp2fit\n'.format(basis))
        out_file.write('set,jkfit\n')
        out_file.write('default,{:s}/jkfit\n'.format(basis))
        out_file.write('}\n\n')
    elif mixed:
        # TODO Add support for mixed basis
        raise NotImplementedError('Mixed basis has not been implemented yet.')
    else:
        out_file.write('basis={\n')
        out_file.write('default,'+basis+'\n')
        out_file.write('}\n\n')


# Function to write a geometry to an open file
def writeGeom(out_file,geometry,atom_labels):
    out_file.write('geometry={\n')
    i = 0
    for item in geometry:
        atom_str = item[0]
        if atom_labels[i] != 0:
            atom_str = atom_str + str(atom_labels[i])
        out_file.write('{0:7s} {1:10.5f} {2:10.5f} {3:10.5f}\n'.format(atom_str,item[1][0],item[1][1],item[1][2]))
        i += 1
    out_file.write('}\n\n')


# Calculate the memory needed by the molpro input file
def calcMolMem(batch_mem,num_cpus):
    return int((batch_mem/num_cpus - 3600)/8)
