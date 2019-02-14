# Script to generate Molpro input files for the WCCR10 project


# What do I need?
# - molecule info (mol_info)
# - basis (basis)
# - memory to allocate per processor in megawords (memory)
# - orbital convergence threshold (orb_thresh)
# - name of file to be saved (file_name)
# - name of file to be saved (file_path)

import os
import input_utils

def make_molpro_input_mp2(mol_info,file_path,file_name,
                       basis='def2-tzvpp',
                       memory=2000,orb_thresh='1d-7'):


    with open(os.path.join(file_path,file_name),'w') as file1:

        # Write header information
        file1.write('!{}\n'.format(file_name))
        file1.write('memory,{:d},M\n\n'.format(memory))
        file1.write('{{gthresh,orbital={}}}\n'.format(orb_thresh))
        file1.write('{symmetry,nosym}\n\n')

        # Write geometry
        atom_labels = mol_info['atom_labels']
        geometry = mol_info['geometry']
        input_utils.writeGeom(file1,geometry,atom_labels)

        # Write basis set
        input_utils.writeBasis(file1,basis)

        # Write high proc
        file1.write('{{df-HF;wf,charge={0}}}\n'.format(mol_info['charge']))
        file1.write('{df-MP2}')
