# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 12:38:55 2015

@author: udothemath1984
"""
import amcsd_list_for_cif
import re

# Entire list
name_list = amcsd_list_for_cif.get_list()
print name_list 

dic_book = {}

print "Hello"

for name in name_list:

    # cif name of the materials 
    print name
    count_indices = amcsd_list_for_cif.get_materials_count_and_indices_with_cif(name)
    print count_indices[1] # Show first dataset
     
#==============================================================================
#     # cif file index 
#     current_cif = amcsd_list_for_cif.get_into_cif_file(count_indices[1])[:8] 
#     print current_cif
#==============================================================================
    
    
    info = amcsd_list_for_cif.get_info_from_cif(count_indices[1])    
    print info.cellparam
    
#==============================================================================
# 
#     # Search for the block contains certain pattern       
#     # http://stackoverflow.com/questions/7421621/python-read-through-file-until-match-read-until-next-pattern
#     block_top='data_global'   
#     block_bot='_journal_name_full'   
#     print amcsd_list_for_cif.pattern_finder(current_cif, block_top, block_bot)
#==============================================================================
 
    # Save the info into dictionary
    dic_book[name] = count_indices     
#print dic_book    


