from setuptools import setup , find_packages
from typing import List


## Declaring Variables for setup file
Project_Name = "housing-Predictor"
Version = "0.0.1"
Author = "Amit Kumar Sahu"
Description = "This is FSDS Nov Batch first Machine Learning Project(End to End"
##Folder = ["housing"]
Requirement_File = "requirements.txt"

def get_requirements_list() -> List[str]:
    """
    Description : This Function is going to return a list of  requirements mention in requirements.txt file
    Return : This function will return a list contains in requirements.txt file 
    
    """
    with open(Requirement_File) as requirement_file :
        return requirement_file.readlines()

setup(
name=Project_Name,
version=Version,
author=Author,
description=Description,
packages=find_packages(), ## In this line we can add find_packages() instead of Folder Variable 
install_requires = get_requirements_list()
)