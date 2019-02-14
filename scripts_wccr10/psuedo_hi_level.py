#!/usr/bin/env python

# Top level python script to create all necessary input files for the WCCR10 project

import input_utils
import read_output
from make_molpro_input_mp2 import *
from make_molpro_input_rpa import *
import os

def main(rxn_key,rxn_dict,cluster,
         high_theory,geom,
         read_output):

    # Determine which cluster is being used
    if cluster == 'cori':
        # TODO This needs to be made
        import make_cori_sbatch
        base_dir = make_cori_sbatch.base_dir
        qos = make_cori_sbatch.qos_premium
        batch_mem = make_cori_sbatch.batch_mem
        #high_num_cpus = 3
        #mol_mem = input_utils.calcMolMem(batch_mem,high_num_cpus)
    elif cluster == 'central':
        # TODO This needs to be made
        import make_central_sbatch
        base_dir = make_central_sbatch.base_dir
        queue = make_central_sbatch.queue_any
        batch_mem = make_central_sbatch.batch_mem
        #high_num_cpus = 3
        #mol_mem = input_utils.calcMolMem(batch_mem,high_num_cpus)
    else: # For tachus case
        import make_tachus_sbatch
        base_dir = make_tachus_sbatch.base_dir
        queue = make_tachus_sbatch.queue_cluster
        batch_mem = make_tachus_sbatch.batch_mem
        high_num_cpus = 3
        mol_mem = input_utils.calcMolMem(batch_mem,high_num_cpus)

    for high_item in high_theory:
        high = high_item[0]
        bs = high_item[1]
        if (not high == 'MP2') and (not "RPA" in high):
            raise ValueError('The specified high-level of theory is not supported. Theory: {:s}'.format(high))

        for mol_key in rxn_dict:
            mol_dict = rxn_dict[mol_key]
            # Create part of file_path
            geom_str=geom[0]+'_geom'
            high_str='df-'+high+'_'+bs
            path = os.path.join(base_dir,rxn_key,high_str,geom_str,mol_key)

            if (read_output):
                # Checks that the directory path already exists
                if not os.path.isdir(path):
                    raise RuntimeError('The specified level theory has not been run. Theory: {:s}'.format(high_str))

                # Create name of output file
                molpro_out = '{0}.out'.format(mol_key)
                if not os.path.isfile(path):
                    raise RuntimeError('Even though the path exists, there is no output file. Path: {:s}'.format(path))

                # Read the output file
                # TODO Perform a check to see if the job finished successfully
                #      Or perform this check in read_output and populate an empty dictionary if output file didn't finish
                if high == 'MP2':
                    key_word = high
                elif 'RPA' in high:
                    key_word = high
                #read_output.readOutput(key_word)

            else:
                # Make directories for the new jobs
                try:
                    os.makedirs(path)
                except OSError:
                    pass

                # Create file names
                molpro_name = '{0}.mol'.format(mol_key)
                batch_name = '{0}.batch'.format(mol_key)
                job_name = mol_key + '_' + high_str
                # Create the batch files depending on the cluster
                if cluster == 'cori':
                    # TODO This needs to be set up still
                    #make_cori_sbatch.main(path,batch_name,job_name,queue,
                    #                    high_num_cpus,batch_mem,molpro_name)
                    pass
                elif cluster == 'central':
                    # TODO This needs to be set up still
                    #make_central_sbatch.main(path,batch_name,job_name,queue,
                    #                       high_num_cpus,batch_mem,molpro_name)
                    pass
                else:
                    make_tachus_sbatch.main(path,batch_name,job_name,queue,
                                          high_num_cpus,batch_mem,molpro_name)

                if high == 'MP2':
                    # Create the df-MP2 inputs
                    make_molpro_input_mp2(mol_dict,path,molpro_name,
                                       basis=bs,memory=mol_mem)
                elif "RPA" in high:
                    # Create the RPA inputs
                    make_molpro_input_rpa(mol_dict,path,molpro_name,
                                       high,basis=bs,memory=mol_mem)
