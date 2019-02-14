#!/usr/bin/env python

# Rerun MP2-in-DFT on reaction with even-handed AO truncation

import input_utils
import ao_union
from rxn_info import all_rxn_dict
from make_molpro_input_embed import *
from make_molpro_input_mp2 import *

import os

def main(rxn_key,rxn_dict,cluster,
         embed_theory,geom,
         trunc_thresh,
         read_output):

    # Determine which cluster is being used
    # TODO Use adapter pattern to create a makeSbatch class
    # TODO Use factory pattern to instantiate makeSbatch class
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

    # Make input files for MP2-in-DFT on reaction with even-handed AO truncation
    for embed_item in embed_theory:
        high = embed_item[0]
        low = embed_item[1]
        bs = embed_item[2]
        for trunc in trunc_thresh:
            old_path_to_reac = []
            old_path_to_prod = []
            new_path_to_reac = []
            new_path_to_prod = []
            # Counter for the number of keys in the rxn_dict
            key_counter = 0
            for mol_key in rxn_dict:
                key_counter += 1
                mol_dict = rxn_dict[mol_key]

                # Create part of file_path
                embed_str=high+'_'+low+'_'+bs
                geom_str=geom[0]+'_geom'
                rxn_a_size_str = str(mol_dict['rxn_a_size']) + '_atoms'
                path = os.path.join(base_dir,rxn_key,embed_str,geom_str,rxn_a_size_str)
                # Create file names
                molpro_name = '{0}.mol'.format(mol_key)
                batch_name = '{0}.batch'.format(mol_key)
                job_name = mol_key + '_' + embed_str

                # Skip loop iteration if trunc == 0 since no need to AO unionize
                if trunc == 0:
                    continue
                # Finish creating file_path
                elif trunc != 0:
                    old_trunc_str = 'ao_trunc_{:.0e}'.format(trunc)
                    new_trunc_str = 'union_ao_trunc_{:.0e}'.format(trunc)

                # Create the paths to the finished jobs and the paths to the new jobs.
                # Separate into prods and reacs.
                old_path_final = os.path.join(path,old_trunc_str,mol_key)
                new_path_final = os.path.join(path,new_trunc_str,mol_key)
                if 'fragment' in mol_key:
                    old_path_to_reac.append(old_path_final)
                    new_path_to_reac.append(new_path_final)
                else:
                    old_path_to_prod.append(old_path_final)
                    new_path_to_prod.append(new_path_final)

                if (read_output):
                    # Checks that the directory path already exists
                    if not os.path.isdir(path):
                        raise RuntimeError('The specified level theory has not been run. Theory: {:s}'.format(embed_str))

                else:
                    # Make directories for the new jobs
                    try:
                        os.makedirs(new_path_final)
                    except OSError:
                        pass

                    # Create the batch files depending on the cluster
                    if cluster == 'cori':
                        # TODO This needs to be set up still
                        #make_cori_sbatch.main(path_final,batch_name,job_name,qos,
                        #                    num_cpus,batch_mem,molpro_name)
                        pass
                    elif cluster == 'central':
                        # TODO This needs to be set up still
                        #make_central_sbatch.main(path_final,batch_name,job_name,queue,
                        #                       num_cpus,batch_mem,molpro_name)
                        pass
                    else:
                        make_tachus_sbatch.main(new_path_final,batch_name,job_name,queue,
                                              embed_num_cpus,batch_mem,molpro_name,trunc_space=True)

                    # Create AO even-handed embed energy inputs
                    make_molpro_input_embed(mol_dict,new_path_final,molpro_name,
                                         basis=bs,
                                         memory=mol_mem,
                                         trunc_thresh=trunc,trunc_space=True,
                                         low_level=low,hi_level=high)

                    # Create the ao union trunction list
                    if key_counter == len(rxn_dict):
                        (reac_aos_union,prod_aos_union) = ao_union.main(old_path_to_reac,old_path_to_prod)
                        # Write the AO list to file to be loaded by Molpro
                        for i in range(len(new_path_to_reac)):
                            with open(os.path.join(new_path_to_reac[i],'trunc_space.txt'),'w') as file1:
                                file1.write( str(len(reac_aos_union[i])) + '\n' )
                                for j in range(len(reac_aos_union[i])):
                                    file1.write( str(reac_aos_union[i][j]) + '\n' )
                        # Write the AO list to file to be loaded by Molpro
                        for i in range(len(new_path_to_prod)):
                            with open(os.path.join(new_path_to_prod[i],'trunc_space.txt'),'w') as file1:
                                file1.write( str(len(prod_aos_union[i])) + '\n' )
                                for j in range(len(prod_aos_union[i])):
                                    file1.write( str(prod_aos_union[i][j]) + '\n' )
