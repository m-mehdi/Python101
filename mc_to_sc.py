#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 20:23:35 2018

@author: joshua

# MC to SC converter.

We can use "# MC" on top of each cell in which we provide answers that we do
not want to share with the students.

This way the MC version is the source of truth and when its done or there are changes
we can use this script to generate the new SC version out of the MC version.

# Steps

- Takes a ipynb file
- Removes all the cells that start with "# MC"
- Removes the execution counts and the outputs of the other cells
- Stores file as _SC.ipynb
    - if original ends with _MC its replaced by _SC, otherwise _SC is added
    
# How to use
    
- Create alias
    - open .profile
        cd ~
        subl .profile
    - add line 
        alias mc_to_sc="[folder script location]/mc_to_sc.py"
- Change permissions of the file
    - go to folder where this script resides
      cd [folder script location]
    - change permission
      chmod 777 mc_to_sc.py
- Convert MC to SC
    - go to folder with the MC notebook
        cd [folder notebook location]
    - run the script against the MC notebook you want to convert
        mc_to_sc My_Notebook_MC.ipynb
    - now My_Notebook_SC.ipynb is generated!
"""

import json
import sys


def is_mc_cell(text):

    text = text.lower()
    mc_tags = ["#MC","# MC", "MC"]

    for tag in mc_tags:
        if text.lower().strip().startswith(tag.lower()):
            print("## REMOVE")
            print(text)
            return True
    
    return False


def mc_to_sc(file_mc, file_sc):
    
    with open(file_mc) as f:
        data = json.load(f)
    
    cells = data['cells']
    cells_new = []
    
    counter=0
    for cell in cells:
        if cell['source']:
            cell_content = cell['source'][0]
            if not is_mc_cell(cell_content):
                if 'outputs' in cell:
                    cell['outputs'] = []
                if 'execution_count' in cell:
                    cell['execution_count'] = None
                cells_new.append(cell)
            else:
                counter+=1
    
    data['cells'] = cells_new
    
    with open(file_sc, 'w') as outfile:
        json.dump(data, outfile, indent=4)
        
    print("Done! Removed %d cells from the MC" % counter)


def get_sc(mc_notebook):
        
    if mc_notebook.endswith("_MC.ipynb"):
        return mc_notebook.replace("_MC.ipynb", "_SC.ipynb")
    
    return mc_notebook.replace(".ipynb", "_SC.ipynb")


if __name__ == "__main__":
    notebook_mc = sys.argv[1]
    notebook_sc = get_sc(notebook_mc)
    mc_to_sc(notebook_mc, notebook_sc)
