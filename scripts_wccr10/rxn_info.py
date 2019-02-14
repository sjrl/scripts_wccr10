from read_xyz import *
# Initialization of the dictionaries
all_rxn_dict = {}

rxn1_dict = {}
rxn1_complex_dict = {}
rxn1_fragment1_dict = {}
rxn1_fragment2_dict = {}

rxn2_dict = {}
rxn2_complex_dict = {}
rxn2_fragment1_dict = {}
rxn2_fragment2_dict = {}

rxn3_dict = {}
rxn3_complex_dict = {}
rxn3_fragment1_dict = {}
rxn3_fragment2_dict = {}

rxn4_dict = {}
rxn4_complex_dict = {}
rxn4_fragment1_dict = {}
rxn4_fragment2_dict = {}

rxn5_dict = {}
rxn5_complex_dict = {}
rxn5_fragment1_dict = {}
rxn5_fragment2_dict = {}

rxn6_dict = {}
rxn6_complex_dict = {}
rxn6_fragment1_dict = {}
rxn6_fragment2_dict = {}

rxn7_dict = {}
rxn7_complex_dict = {}
rxn7_fragment1_dict = {}
rxn7_fragment2_dict = {}

rxn8_dict = {}
rxn8_complex_dict = {}
rxn8_fragment1_dict = {}
rxn8_fragment2_dict = {}

rxn9_dict = {}
rxn9_complex_dict = {}
rxn9_fragment1_dict = {}
rxn9_fragment2_dict = {}

rxn10_dict = {}
rxn10_complex_dict = {}
rxn10_fragment1_dict = {}
rxn10_fragment2_dict = {}


# Fill in dictionaries with reaction specific info
rxn7_complex_dict['geometry'] = read_xyz('/home/sjlee/projects/wccr10/coordinates/7complex_bp86.xyz')
rxn7_complex_dict['atom_labels'] = [1,1,1,2,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,0,0,0,0,0,0,0,0]
rxn7_complex_dict['atoms_in_a'] = '[Cu1,C1,N1,N2,N3,N4,C2,C3]'
rxn7_complex_dict['rxn_a_size'] = 8
rxn7_complex_dict['core_in_a'] = 16
rxn7_complex_dict['charge'] = 1

rxn7_fragment1_dict['geometry'] = read_xyz('/home/sjlee/projects/wccr10/coordinates/7fragment1_bp86.xyz')
rxn7_fragment1_dict['atom_labels'] = [1,1,1,2,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
rxn7_fragment1_dict['atoms_in_a'] = '[Cu1,C1,N1,N2,C2,C3]'
rxn7_fragment1_dict['rxn_a_size'] = 8
rxn7_fragment1_dict['core_in_a'] = 14
rxn7_fragment1_dict['charge'] = 1

rxn7_fragment2_dict['geometry'] = read_xyz('/home/sjlee/projects/wccr10/coordinates/7fragment2_bp86.xyz')
rxn7_fragment2_dict['atom_labels'] = [1,2,0,0,0,0,0,0,0,0]
rxn7_fragment2_dict['atoms_in_a'] = '[N1,N2]'
rxn7_fragment2_dict['rxn_a_size'] = 8
rxn7_fragment2_dict['core_in_a'] = 2
rxn7_fragment2_dict['charge'] = 0

rxn7_dict['7complex'] = rxn7_complex_dict
rxn7_dict['7fragment1'] = rxn7_fragment1_dict
rxn7_dict['7fragment2'] = rxn7_fragment2_dict


# Assemble final dictionary that I want to use --> mol_info_dict
#all_rxn_dict['rxn1'] = rxn1_dict
#all_rxn_dict['rxn2'] = rxn2_dict
#all_rxn_dict['rxn3'] = rxn3_dict
#all_rxn_dict['rxn4'] = rxn4_dict
#all_rxn_dict['rxn5'] = rxn5_dict
#all_rxn_dict['rxn6'] = rxn6_dict
all_rxn_dict['rxn7'] = rxn7_dict
#all_rxn_dict['rxn8'] = rxn8_dict
#all_rxn_dict['rxn9'] = rxn9_dict
#all_rxn_dict['rxn10'] = rxn10_dict
