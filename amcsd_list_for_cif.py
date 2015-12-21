# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 12:25:20 2015

@author: udothemath1984
"""
import scraperwiki
import lxml.html
import re

class CifInfo:
    #
    # just for convenience
    def __init__(self):
        self.cellparam = [None] * 10
        self.spacegroup = ''


def get_list():
    # https://pypi.python.org/pypi/scraperwiki
    # pip install scraperwiki
    html_site = scraperwiki.scrape('http://rruff.geo.arizona.edu/AMS/all_minerals.php')
    #print html_site
    # http://lxml.de/lxmlhtml.html
    root = lxml.html.fromstring(html_site)
    # Find all the links in the webpage html_site    
        
    # get the links
    # Eventually, hrefs give the list in the format /AMS/minerals/XXX_materials 
    # http://stackoverflow.com/questions/21455349/xpath-query-get-attribute-href-from-a-tag
    n_data_set = 2        
        
    all_hrefs = root.xpath('//a/@href')[:n_data_set+1]    
    del all_hrefs[0]    # First one in the list is always /AMS/amcsd.php    
    data_name = []

    # This is for capturing name of the materials
    for href in all_hrefs:        
        data_name.append( href.split('/')[-1] )

    #print data_name
    return data_name

def get_materials_count_and_indices_with_cif(name=''): 

    html_here = scraperwiki.scrape( 'http://rruff.geo.arizona.edu/AMS/minerals/{0}'.format(name))
    root = lxml.html.fromstring(html_here)
    hrefs = root.xpath('//a/@href')
    #print hrefs
    # hrefs give all the available links from page html_here
        
    data_count_and_indices = []
    #https://docs.python.org/2/howto/regex.html
    p = re.compile('\d+') # find matching pattern
    # Looking for index for cif files
    for href in hrefs:  
        if '/AMS/download.php?id=' and '.cif&down=cif' in href:
            data_count_and_indices = data_count_and_indices + p.findall(href)
    data_count_and_indices.insert(0, len(data_count_and_indices))
    #print data_count_and_indices, [number, first_evidence, second_evidence, ...]
    return data_count_and_indices

def get_into_cif_file(material_index=''): 
    import urllib2
    cif_info = urllib2.urlopen('http://rruff.geo.arizona.edu/AMS/CIF_text_files/{0}_cif.txt'.format(material_index)) 
    # Remove \n  
    #http://stackoverflow.com/questions/12330522/reading-a-file-without-newlines
    access_cif = cif_info.read().splitlines()   
    # Remain \n    
    #access_cif = cif_info.readlines()  
    return access_cif


def get_info_from_cif(material_index=''): 
    import urllib2
    cif_info = urllib2.urlopen('http://rruff.geo.arizona.edu/AMS/CIF_text_files/{0}_cif.txt'.format(material_index)) 
    # Remove \n  
    #http://stackoverflow.com/questions/12330522/reading-a-file-without-newlines
    access_cif = cif_info.read().splitlines()
    cif_info = CifInfo()    
    
    for item in access_cif[:40]: 
        if '_cell_length_a' in item:
            cif_info.cellparam[0] = item.split()[1]
        if '_cell_length_b' in item:
            cif_info.cellparam[1] = item.split()[1]
        if '_cell_length_c' in item:
            cif_info.cellparam[2] = item.split()[1]
        if '_cell_angle_alpha' in item:
            cif_info.cellparam[3] = item.split()[1]
        if '_cell_angle_beta' in item:
            cif_info.cellparam[4] = item.split()[1]
        if '_cell_angle_gamma' in item:
            cif_info.cellparam[5] = item.split()[1]
        if '_cell_volume' in item:
            cif_info.cellparam[6] = item.split()[1]            
        if '_exptl_crystal_density_diffrn' in item:
            cif_info.cellparam[7] = item.split()[1]            
                        
    return cif_info
    
 
def pattern_finder(read_list, start='',end=''):
    import re
    linestop = 0
    pattern_block = []
    for line in read_list:
        if linestop == 0:
            if re.match(start, line):
                #print line
                linestop = 1            
        else:
            if re.match(end, line):
                linestop = 0
            else:
                pattern_block.append(line)
    return pattern_block 
        
       
    
    
