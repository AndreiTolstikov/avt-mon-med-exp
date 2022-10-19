"""
Prepare domain data from "domains_data.json" file for further processing
"""

import json
import os


def load_domains_data(domains_data_file_name):
    """
    Load domain data from JSON file (by default "domains_data.json") 
    for further processing
    
    Returns:
        [dict] -- domain data in Python dictionary format
    """

    # The directory that contains the executable file of the project(avtmonexp.py)
    # will be made current
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # open domains data file (by default "domains_data.json") for parsing
    full_file_name = os.path.abspath(domains_data_file_name)
    try:
        file_handler = open(full_file_name,'r', encoding='utf-8')
    except:
        print('File cannot be opened:', full_file_name)
        exit()

    # read the whole domains data file (by default "domains_data.json")
    try:
        domains_data = file_handler.read()

        # close file handler
        file_handler.close()

    except:
        print("File cannot be read: ", full_file_name)
        exit()

    # load domains_data in JSON format
    all_domains_json = json.loads(domains_data)
    
    return all_domains_json
