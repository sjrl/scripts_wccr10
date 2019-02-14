# Script to generate Molpro input files for the WCCR10 project


# What do I need?
# - molecule info (mol_info)
# - basis (basis)
# - evaluate force? (eval_force)
# - memory to allocate per processor in megawords (memory)
# - orbital convergence threshold (orb_thresh)
# - grid index to use for Neese grid (neese_index)
# - truncation threshold (trunc_thresh)
# - high level of theory (hi_level)
# - low level of theory (low_level)
# - name of file to be saved (file_name)
# - name of file to be saved (file_path)


import os
import input_utils

def make_molpro_input_embed(mol_info,file_path,file_name,
                         basis='def2-tzvpp',
                         eval_force=False,gdirect=True,
                         memory=2000,orb_thresh='1d-7',neese_index=4,
                         trunc_thresh=0,trunc_space=False,
                         low_level='PBE',hi_level='MP2'):

    # Determine whether or not RPA is being called
    rpa=False
    if "RPA" in hi_level:
        rpa=True

    # Write the emebdding input file
    with open(os.path.join(file_path,file_name),'w') as file1:

        # Write header information
        file1.write('!{}\n'.format(file_name))
        file1.write('memory,{:d},M\n'.format(memory))
        if gdirect:
            file1.write('GDIRECT\n')
        file1.write('\n')
        file1.write('{{gthresh,orbital={}}}\n'.format(orb_thresh))
        file1.write('{{grid,name=NEESE,neese_index={:d}}}\n\n'.format(neese_index))
        file1.write('{symmetry,nosym}\n\n')

        # Write geometry
        atom_labels = mol_info['atom_labels']
        geometry = mol_info['geometry']
        input_utils.writeGeom(file1,geometry,atom_labels)

        # Write basis set
        input_utils.writeBasis(file1,basis,rpa=rpa)

        # Write low proc
        core_in_a = mol_info['core_in_a']
        if trunc_thresh != 0:
            file1.write('proc low\n')
            file1.write('   {{df-hf,hf_cor=0;core,{0};save,2103.2;start,2103.2}}\n'.format(core_in_a))
            file1.write('   {{df-rks,{0},hf_cor=0;core,{1};save,2104.2;start,2103.2}}\n'.format(low_level,core_in_a))
            file1.write('   {{rks,{0},hf_cor=0;core,{1};save,2105.2;start,2104.2}}\n'.format(low_level,core_in_a))
            if eval_force:
                file1.write('   {force,gridgrad=1}\n')
            file1.write('endproc\n\n')

        # Write high proc
        # TODO Missing save option for CCSD (for T amplitudes)
        file1.write('proc hi\n')
        if rpa:
            file1.write('   {{df-rks,pbe,hf_cor=0,basis=jkfit;core,{0};save,2106.2;start,2103.2}}\n'.format(core_in_a))
        else:
            file1.write('   {{HF,hf_cor=0;core,{0};save,2106.2;start,2103.2}}\n'.format(core_in_a))
        file1.write('   {{{0};core,{1};cphf,thrmin=1.d-7}}\n'.format(hi_level,core_in_a))
        if eval_force:
            file1.write('   {force}\n')
        file1.write('endproc\n\n')

        # Write low level calc
        file1.write('{{df-hf;wf,charge={0};core,0;save,2100.2;start,2100.2}}\n'.format(mol_info['charge']))
        file1.write('{{df-rks,{0};save,2101.2;start,2100.2}}\n'.format(low_level))
        file1.write('{{rks,{0};save,2102.2;start,2101.2}}\n\n'.format(low_level))

        # Write localization method
        file1.write('{locali,pipek;core,0}\n')

        # Write embed command
        atoms_in_a = mol_info['atoms_in_a']
        if eval_force:
            #FIXME Turning direct off here does not work for normal embedding w/o AO truncation
            #embed_str = '{{embed,grad,direct_off,highproc=hi,atoms={0},print=2\n'.format(atoms_in_a)
            embed_str = '{{embed,grad,highproc=hi,atoms={0},print=2\n'.format(atoms_in_a)
            if trunc_thresh != 0:
                if trunc_space:
                    embed_str = "{{embed,grad,direct_off,highproc=hi,atoms={0},print=2,truncate={1},loadao='../trunc_space.txt',lowproc=low,ao_per_atom,storeao\n".format(atoms_in_a,trunc_thresh)
                else:
                    embed_str = "{{embed,grad,direct_off,highproc=hi,atoms={0},print=2,truncate={1},lowproc=low,ao_per_atom,storeao\n".format(atoms_in_a,trunc_thresh)
            file1.write(embed_str)
            file1.write('local,cplsolve=1}\n')
            file1.write('{force,gridgrad=1}')
        else:
            #FIXME Turning direct off here does not work for normal embedding w/o AO truncation
            #embed_str = '{{embed,direct_off,highproc=hi,atoms={0},print=2}}\n'.format(atoms_in_a)
            embed_str = '{{embed,highproc=hi,atoms={0},print=2}}\n'.format(atoms_in_a)
            if trunc_thresh != 0:
                if trunc_space:
                    embed_str = "{{embed,direct_off,highproc=hi,atoms={0},print=2,truncate={1},loadao='../trunc_space.txt',lowproc=low,ao_per_atom,storeao}}\n".format(atoms_in_a,trunc_thresh)
                else:
                    embed_str = "{{embed,direct_off,highproc=hi,atoms={0},print=2,truncate={1},lowproc=low,ao_per_atom,storeao}}\n".format(atoms_in_a,trunc_thresh)
            file1.write(embed_str)
