import re
import os
import numpy as np
import xml.etree.ElementTree as ET
import sys
import random


print("Let's change the config file.\n")

# path = os.getcwd()
# up_dir = os.path.dirname(path)
# file_name =  os.path.join(up_dir,'py_ref_channel.xml')


def adjust_config_file(new_config, file_path):
    tree = ET.parse(file_path)
    for elem in tree.iterfind(new_config['tree_path']):
        print(elem.tag, elem.attrib)
        elem.set(new_config['attribute'], new_config['new_value'])

    with open(file_path, "wb") as fh:
        tree.write(fh, xml_declaration=True, encoding='utf-8', method="xml")


what = 'GravitationX'
config = {
    'attribute': what,
    'tree_path': 'Model/Params[@%s]' % what,
    'new_value': str(random.randint(10, 100))}

file_name = "sample_case.xml"

adjust_config_file(config, file_name)

tree2 = ET.parse(file_name)
print("--check changes from file--")
for elem in tree2.iterfind(config['tree_path']):
    print(elem.tag, elem.attrib)

print("\nDone")

