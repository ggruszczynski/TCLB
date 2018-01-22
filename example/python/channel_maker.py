
import os
import numpy as np
import xml.etree.ElementTree as ET

import sys

# this script is to make a corrugated channel geometry as in
# "Incompressible LBGK simulation of flow characterisics in a micro-channel with patterned superhydrophobic surfaces"
# by Li Bowen, Yao ZHaoHui, Hao PengFei

# parametes from the article:
L = 3 # length of ridge-wall
S = 6  # length of air-hole
h = 2  # depth of air-hole

channel_length = 256
channel_height = 100 # TODO: put 200

ridges = np.arange(0, channel_length, L + S)

path = os.getcwd()
up_dir = os.path.dirname(path)
# file_name =  os.path.join(up_dir,'py_ref_channel.xml')

file_name = "py_ref_channel.xml"


def indent(elem, level=0):
    '''
    copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
    it basically walks your tree and adds spaces and newlines so the tree is
    printed in a nice way
    '''

    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def _build_BC(geometry_node, model_node):
    return

    inlet = ET.SubElement(geometry_node, "WPressure")
    inlet.set("name", "inlet")
    inlet.set("nx", str(1))
    inlet.set("dx", str(5))
    ET.SubElement(inlet, "Box")

    outlet = ET.SubElement(geometry_node, "EPressure")
    outlet.set("name", "outlet")
    outlet.set("nx", str(1))
    outlet.set("dx", str(-5))
    ET.SubElement(outlet, "Box")

    params = ET.SubElement(model_node, "Params")
    params.set("Pressure", str(0.0001))


def _build_surface(xml_wall_element):
    wall = ET.SubElement(xml_wall_element, "Wall")
    wall.set("mask", "ALL")
    wall.set("name", "bottom_wall")

    box = ET.SubElement(wall, "Box")
    box.set("ny", str(1)) # make bottom_wall

    for ridge in ridges[:-1]: # skip the last ridge
        box = ET.SubElement(wall, "Box")
        box.set("dx", str(ridge))
        box.set("nx", str(L))
        box.set("fy", str(h))


def _build_model(model_node):

    params = ET.SubElement(model_node, "Params")

    density_h = 1
    params.set("Density_h", str(density_h))
    params.set("Density_l", str(0.08))

    params.set("Viscosity_h", str(0.3333333333333333))
    params.set("Viscosity_l", str(0.4166666666666667))

    params.set("PhaseField_init", str(0.0))
    params.set("PhaseField_h", str(1.0))
    params.set("PhaseField_l", str(0.0))

    params.set("ContactAngle", str(45))  # with respect ot high density fluid

    params.set("W", str(5))  # interface width
    params.set("M", str(0.05))  # Mobility
    params.set("sigma", str(5e-5))  # surface tension

    params.set("Period", str(channel_length))
    params.set("Perturbation", str(0.01))
    params.set("MidPoint", str(h))

    params.set("GravitationX", str(0.08*channel_length/density_h))


    indent(params)

def build_channel():

    CLBConfig = ET.Element("CLBConfig")  # root element
    CLBConfig.set("version", "2.0")
    CLBConfig.set("output", "output/")

    # --- geometry --- #
    geometry = ET.SubElement(CLBConfig, "Geometry")
    geometry.set("nx", str(channel_length))
    geometry.set("ny", str(channel_height))

    collision_operator = ET.SubElement(geometry, "MRT")
    ET.SubElement(collision_operator, "Box")

    wall = ET.SubElement(geometry, "Wall")
    wall.set("mask", "ALL")
    wall.set("name", "upper_wall")

    upper_wall = ET.SubElement(wall, "Box")
    upper_wall.set("dy", str(-1))

    model = ET.SubElement(CLBConfig, "Model")

    _build_BC(geometry_node=geometry,
              model_node=model)
    _build_surface(xml_wall_element=geometry)
    _build_model(model_node=model)


    failcheck = ET.SubElement(CLBConfig, "Failcheck")
    failcheck.set("Iterations", str(2000))

    solve = ET.SubElement(CLBConfig, "Solve")
    solve.set("Iterations", str(10000))
    vtk = ET.SubElement(solve, "VTK")
    vtk.set("Iterations", str(2000))
    log = ET.SubElement(solve, "Log")
    log.set("Iterations", str(1000))

    indent(CLBConfig)  # make it pretty print
    tree = ET.ElementTree(CLBConfig)
    with open(file_name, "wb") as fh:
        tree.write(fh, xml_declaration=True, encoding='utf-8', method="xml")


def append_notes_to_file():
    with open(file_name, "a") as f:
        f.write("\n\n"
                "<!-- This is an automatically generated file --> \n"
                "<!-- usage: to test TCLB result against: --> \n"
                "<!--\n'Incompressible LBGK simulation of flow characterisics\n"
                " in a micro-channel with patterned superhydrophobic surfaces'\n "
                "by Li Bowen, Yao ZHaoHui, Hao PengFei \n-->"
                "\n\n<!-- Model:	models/multiphase/d2q9_pf_velocity -->"
                )


'''
main function, so this program can be called by python program.py
'''
if __name__ == "__main__":
    build_channel()
    append_notes_to_file()
