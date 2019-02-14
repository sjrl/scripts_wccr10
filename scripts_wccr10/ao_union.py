""" Module even_handed_ao  

This module provides functions to read in multiple sets of AOs and unionize them.
"""

import os
import copy


def make_ao_dict(filename):
    """
    This function creates and returns an atomic orbital (AO) dictionary.

    Parameters
    ----------
    filename : str
        Filename (with absolute path specified) to be read. Should be a Molpro output file.

    Returns
    -------
    ao_dict : dictionary
    """

    ao_dict = {}
    ao_list = []
    list_start = False
    list_done = False
    counter = 0

    with open(filename,'r') as file1:
        for l,line in enumerate(file1):
            fields = line.split()

            if len(fields) == 8 and fields[0] == 'Active' and fields[1] == 'functions' and fields[2] == 'after':
                list_start = True
                list_done = False
                counter += 1
                ao_list = []
                continue
            elif len(fields) == 6 and fields[0] == 'Number' and fields[1] == 'of' and fields[2] == 'functions' and fields[3] == 'is':
                list_done = True
                list_start = False

            if (not list_done and list_start):
                if len(fields) == 22:
                    for j in range(2,len(fields)):
                        ao_list.append(int(fields[j]))
                elif (len(fields) == 0):
                    pass
                else:
                    for j in range(1,len(fields)):
                        ao_list.append(int(fields[j]))
            elif list_done:
                ao_dict[counter] = ao_list
    return ao_dict


def original_num_aos(filename):
    """
    This function reads the original number of AOs used in the Molpro calculation before AO truncation.

    Parameters
    ----------
    filename : str
        Filename (with absolute path specified) to be read. Should be a Molpro output file.

    Returns
    -------
    num_aos : int
        The original number of AOs used in the calculation before AO truncation.
    """

    num_aos = 0
    l_old = -2

    with open(filename,'r') as file1:
        for l,line in enumerate(file1):
            fields = line.split()

            if len(fields) == 6 and fields[0] == 'Number' and fields[1] == 'of' and fields[2] == 'functions' and fields[3] == 'is':
                l_old = l
            
            if l == (l_old + 1) and len(fields) == 2 and fields[0] == 'Original:':
                num_aos  = int(fields[1])
    return num_aos


def main(path_to_reac,path_to_prod):
    # Collect all the Molpro output files for the reactants
    reac_files = []
    for path in path_to_reac:
        for root, dirs, files in os.walk(path):
            for name in files:
                if (name[-3:] == "out" and name[:3] != "job"):
                    reac_files.append(os.path.join(root,name))

    # Collect all the Molpro output files for the products
    prod_files = []
    for path in path_to_prod:
        for root, dirs, files in os.walk(path):
            for name in files:
                if (name[-3:] == "out" and name[:3] != "job"):
                    prod_files.append(os.path.join(root,name))

    # Creates a list of tuples (num_aos,list_of_truncated_AOs)
    reac_aos = []
    for item in reac_files:
        ao_dict_tmp =  make_ao_dict(item)
        num_aos_tmp = original_num_aos(item)
        reac_aos.append((num_aos_tmp,ao_dict_tmp[1]))
    #print(reac_aos)

    # Creates a list of tuples (num_aos,list_of_truncated_AOs)
    prod_aos = []
    for item in prod_files:
        ao_dict_tmp =  make_ao_dict(item)
        num_aos_tmp = original_num_aos(item)
        prod_aos.append((num_aos_tmp,ao_dict_tmp[1]))

    # NOTE Either assume correct order given when arguments are given or do a sort here.
    #      Most general case is to be given correct order. So not sorting.

    # Create a version of ao_list_reac where the second molecule (e.g. fragment2) is properly 
    # offsetted by first molecule (e.g. fragment1).
    reac_aos_offset = reac_aos.copy()
    for i in range(len(reac_aos_offset[1][1])):
        reac_aos_offset[1][1][i] += reac_aos_offset[0][0]
    #print(reac_aos_offset)

    # NOTE In principle do the same for the products side, but it's a complex so no need to

    # Create two item list to compare reactants (1st item) and products (2nd item)
    compare_aos = []
    compare_aos.append(reac_aos_offset[0][1]+reac_aos_offset[1][1])
    compare_aos.append(prod_aos[0][1])
    #print(compare_aos)

    # Accumulate the AOs between the two lists in compare_aos
    accum = set(compare_aos[0])
    for i in range(1,len(compare_aos)):
        accum = accum | set(compare_aos[i])
    accum = list(accum)
    accum.sort()
    #print(accum)

    # Make reac_aos_union list which contains the reactants in the same order they were provided.
    reac_aos_union = []
    for j in range(len(reac_aos)):
        item = []
        for i in range(len(accum)):
            if j == 0:
                if accum[i] <= reac_aos[j][0]:
                    item.append(accum[i])
            else:
                if accum[i] > reac_aos[j-1][0] and accum[i] <= (reac_aos[j-1][0]+reac_aos[j][0]):
                    item.append(accum[i]-reac_aos[j-1][0])
        reac_aos_union.append(item)
    #print(reac_aos_union)

    # In this case entire accum list is the ao union list for the product
    # NOTE This may not always be the case
    prod_aos_union = []
    prod_aos_union.append(accum)
    #print(prod_aos_union)

    # Print some useful info to screen
    for i in range(len(reac_aos)):
        string1 = "Reactant " + str(i+1) + ": Started with " + str(len(reac_aos[i][1])) + " AOs. Ended with " + str(len(reac_aos_union[i])) + " AOs."
        print(string1)
    for i in range(len(prod_aos)):
        string1 = "Product  " + str(i+1) + ": Started with " + str(len(prod_aos[i][1])) + " AOs. Ended with " + str(len(prod_aos_union[i])) + " AOs."
        print(string1)
    #string = "Accumulated " + str(len(accum)) + " AOs"
    #print(string)

    return (reac_aos_union,prod_aos_union)


#path_to_reac = []
#path_to_reac.append('/home/sjlee/projects/wccr10/rxn7/MP2_PBE_def2-tzvpp/BP86_geom/ao_trunc_1e-03/7fragment1')
#path_to_reac.append('/home/sjlee/projects/wccr10/rxn7/MP2_PBE_def2-tzvpp/BP86_geom/ao_trunc_1e-03/7fragment2')
#path_to_prod = ['/home/sjlee/projects/wccr10/rxn7/MP2_PBE_def2-tzvpp/BP86_geom/ao_trunc_1e-03/7complex']
#
#main(path_to_reac,path_to_prod)
