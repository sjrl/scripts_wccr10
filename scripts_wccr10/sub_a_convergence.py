#!/usr/bin/env python

# Top level python script to create all necessary input files for the WCCR10 project

import input_utils
from make_molpro_input_embed import *
import os

def main(rxn_key,rxn_dict,cluster,
         embed_theory,geom,
         trunc_thresh,
         read_output):

    # Determine which cluster is being used
    if cluster == 'cori':
        # TODO This needs to be made
        import make_cori_sbatch
        base_dir = make_cori_sbatch.base_dir
        qos = make_cori_sbatch.qos_premium
        batch_mem = make_cori_sbatch.batch_mem
        #embed_num_cpus = 6
        #mol_mem = input_utils.calcMolMem(batch_mem,embed_num_cpus)
    elif cluster == 'central':
        # TODO This needs to be made
        import make_central_sbatch
        base_dir = make_central_sbatch.base_dir
        queue = make_central_sbatch.queue_any
        batch_mem = make_central_sbatch.batch_mem
        #embed_num_cpus = 6
        #mol_mem = input_utils.calcMolMem(batch_mem,embed_num_cpus)
    else: # For tachus case
        import make_tachus_sbatch
        base_dir = make_tachus_sbatch.base_dir
        queue = make_tachus_sbatch.queue_cluster
        batch_mem = make_tachus_sbatch.batch_mem
        embed_num_cpus = 3
        mol_mem = input_utils.calcMolMem(batch_mem,embed_num_cpus)
        #embed_num_cpus = 6
        #mol_mem = 900

    for embed_item in embed_theory:
        high = embed_item[0]
        low = embed_item[1]
        bs = embed_item[2]
        for trunc in trunc_thresh:
            for mol_key in rxn_dict:
                mol_dict = rxn_dict[mol_key]

                # Create part of file_path
                embed_str = high + '_' + low + '_' + bs
                geom_str = geom[0] + '_geom'
                rxn_a_size_str = str(mol_dict['rxn_a_size']) + '_atoms'
                path = os.path.join(base_dir,rxn_key,embed_str,geom_str,rxn_a_size_str)
                # Create file names
                molpro_name = '{0}.mol'.format(mol_key)
                batch_name = '{0}.batch'.format(mol_key)
                job_name = mol_key + '_' + embed_str
                # Finish creating file_path
                if trunc == 0:
                    trunc_str = 'ao_trunc_0'
                else:
                    trunc_str = 'ao_trunc_{:.0e}'.format(trunc)
                path_final = os.path.join(path,trunc_str,mol_key)

                if (read_output):
                    # Checks that the directory path already exists
                    if not os.path.isdir(path):
                        raise RuntimeError('The specified level theory has not been run. Theory: {:s}'.format(embed_str))

                else:
                    # Make directories for the new jobs
                    try:
                        os.makedirs(path_final)
                    except OSError:
                        pass

                    # Create the batch files depending on the cluster
                    if cluster == 'cori':
                        # TODO This needs to be set up still
                        #make_cori_sbatch.main(path_final,batch_name,job_name,queue,
                        #                    num_cpus,batch_mem,molpro_name)
                        pass
                    elif cluster == 'central':
                        # TODO This needs to be set up still
                        #make_central_sbatch.main(path_final,batch_name,job_name,queue,
                        #                       num_cpus,batch_mem,molpro_name)
                        pass
                    else:
                        make_tachus_sbatch.main(path_final,batch_name,job_name,queue,
                                              embed_num_cpus,batch_mem,molpro_name)
                    # Create the embedding inputs
                    make_molpro_input_embed(mol_dict,path_final,molpro_name,
                                         basis=bs,
                                         memory=mol_mem,
                                         trunc_thresh=trunc,
                                         low_level=low,hi_level=high)
