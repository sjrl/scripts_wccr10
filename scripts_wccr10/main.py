#!/usr/bin/env python

# Top level python script to create all necessary input files for the WCCR10 project

from rxn_info import all_rxn_dict
import psuedo_hi_level
import sub_a_convergence
import even_handed_ao
import os
import argparse

def main(rxn_keys,hi_level,low_level,basis,geom,loc_space,trunc_thresh,
         cluster='tachus',
         convergence_check=False,convergence_check_even_handed=False,
         embedding_energy=False,embedding_optimization=False,
         read_output=False):

    # Do some initial parsing
    hi_level = [high.upper() for high in hi_level]
    low_level = [low.upper() for low in low_level]
    basis = [bs.lower() for bs in basis]

    # Create all possible combinations of theories
    high_theory = []
    embed_theory = []
    for high in hi_level:
        for bs in basis:
            high_item = [high,bs]
            high_theory.append(high_item)
    for high in hi_level:
        for low in low_level:
            for bs in basis:
                embed_item = [high,low,bs]
                embed_theory.append(embed_item)

    # - Do convergence check
    #   1) Run df-MP2 reaction
    #   2) Run MP2-in-DFT on reaction to check Sub A size
    #   2a) Run MP2-in-DFT on reaction at various truncation thresholds
    if convergence_check:
        for rxn_key in rxn_keys:
            rxn_dict = all_rxn_dict[rxn_key]
            psuedo_hi_level.main(rxn_key,rxn_dict,cluster,
                                 high_theory,geom,
                                 read_output)
            sub_a_convergence.main(rxn_key,rxn_dict,cluster,
                                   embed_theory,geom,
                                   loc_space,
                                   trunc_thresh,
                                   read_output)

    #   2b) Rerun MP2-in-DFT on reaction with even-handed AO truncation
    elif convergence_check_even_handed:
        for rxn_key in rxn_keys:
            rxn_dict = all_rxn_dict[rxn_key]
            even_handed_ao.main(rxn_key,rxn_dict,cluster,
                              embed_theory,geom,
                              trunc_thresh)

    # - Once convergence check finished do energy calculations
    #   1) Run CCSD-in-DFT with correct sub A size and even-handed AO
    #   1a) Check T1 and D1 diagnostics
    #   2) Run CCSD(T)-in-DFT with correct sub A size and even-handed AO
    elif embedding_energy:
        pass


    # - In parallel do geometry optimization
    #   1) Optimize at CCSD-in-DFT with correct sub A size and even-handed AO
    #   2) Run CCSD(T)-in-DFT on optimized geometries with correct sub A size and even-handed AO
    elif embedding_optimization:
        pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rxn', type=str, default=None, action='append', help='Specify reactions to study.', required=True)
    #parser.add_argument('--high', type=str, default=None, help='Specify high-level of theory.',required=True)
    #parser.add_argument('--low',  type=str, default=None, help='Specify low-level of theory.',required=True)
    #parser.add_argument('--basis',type=str, default=None, help='Specify basis set.',required=True)
    parser.add_argument('--subA',  type=bool, default=False,    help='Subsystem A convergence check.')
    parser.add_argument('--even',  type=bool, default=False,    help='Even-handed convergence check.')
    parser.add_argument('--energy',type=bool, default=False,    help='Calculate embedding energy.')
    parser.add_argument('--opt',   type=bool, default=False,    help='Do embedding gradient optimization.')
    parser.add_argument('--cluster',type=str, default='tachus', help='Specify HPC cluster.')
    #parser.add_argument('--queue', type=str, default='CLUSTER', action='append', help='Specify HPC queue.')
    parser.add_argument('--readOut',type=bool, default=False,   help='Read Molpro output files corresponding one of the types of calculations.')
    args = parser.parse_args()
    rxn_keys = args.rxn
    #hi_level = args.high
    #low_level = args.low
    #basis = args.basis
    subA_check = args.subA
    even_check = args.even
    energy_calc = args.energy
    opt_calc = args.opt
    cluster_type = args.cluster
    read_output = args.readOut

    if (not subA_check and not even_check and not energy_calc and not opt_calc):
        raise RuntimeError('Need to provide one of the arguments --subA, --even, --energy, or --opt.')

    hi_level = [x for x in input('Enter high-level of theory: ').split()]
    low_level = [x for x in input('Enter low-level of theory: ').split()]
    basis = [x for x in input('Enter basis set: ').split()]
    loc_space = input('Enter localization space: ')
    if len(hi_level) == 0 or len(low_level) == 0 or len(basis) == 0:
        raise RuntimeError('Please provide at least one input for high-level, low-level and basis.')
    geom = ['BP86']
    trunc_thresh=[0,1e-1,1e-2,1e-3,1e-4,1e-5]

    main(rxn_keys,hi_level,low_level,basis,
         geom,loc_space,trunc_thresh,
         cluster=cluster_type,
         convergence_check=subA_check,convergence_check_even_handed=even_check,
         embedding_energy=energy_calc,embedding_optimization=opt_calc,
         read_output=read_output)
