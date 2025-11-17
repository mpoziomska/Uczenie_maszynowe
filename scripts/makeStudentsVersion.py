#!/bin/python3

import os
import subprocess
import glob
from termcolor import colored
import nbformat

testRun = False

result = subprocess.run(["git", "branch","--show-current"], text=True, capture_output=True)
branch_name = result.stdout
branch_name = branch_name.rstrip("\n")

print(colored(f"Commiting curent changes to solution branch {branch_name}.","blue"))
if not testRun:
    subprocess.run(["git", "commit","-a", "-m automatic commit"])

print(colored("Switching to students branch.","blue"))
students_branch_name = branch_name.replace("_solutions","")
if not testRun:
    result = subprocess.run(["git", "checkout",students_branch_name], text=True, capture_output=True)
print(colored("Removing solutions blocks.","blue"))

# result = subprocess.run(["git","diff","--name-only", branch_name, students_branch_name], text=True, capture_output=True)
# fileList = result.stdout.rstrip("\n").split("\n")
# print(result, fileList)
fileList = ['08_Drzewa_decyzyjne.ipynb', '09_Drzewa_decyzyjne.ipynb']

def strip_solutions(input_file, output_file):
    nb = nbformat.read(input_file, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            new_source = []
            p = False
            for line in cell.source.splitlines(keepends=True):
                if "#BEGIN_SOLUTION" in line:
                    p = True
                    new_source.append("...\n")  # placeholder
                    continue
                if "#END_SOLUTION" in line:
                    p = False
                    continue
                if not p:
                    new_source.append(line)
            cell.source = "".join(new_source)
    nbformat.write(nb, output_file)

for aFile_name in fileList:
    if aFile_name.find("README")!=-1 or  aFile_name.find("makeStudentsVersion.py")!=-1:
        continue
    print(colored(f"Processing file {aFile_name}","green"))
    input_file_name = aFile_name
    # output_file = open("tmp.ipynb", "w")
    subprocess.run(["git","restore", "--source",branch_name,"--",aFile_name], text=True, capture_output=True)
    result = subprocess.run(["git","add",aFile_name], text=True, capture_output=True)
    strip_solutions(input_file_name, "tmp.ipynb")
    if not testRun:
        subprocess.run(["mv","tmp.ipynb",input_file_name])
    
print(colored("Commiting curent changes to students branch.","blue"))
if not testRun:
    subprocess.run(["git", "status"])
    subprocess.run(["git", "commit","-a", "-m automatic commit"])

print(colored("Switching back to solutions branch.","blue"))
if not testRun:
    subprocess.run(["git", "checkout",branch_name], text=True, capture_output=True)
