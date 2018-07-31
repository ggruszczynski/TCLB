#!/usr/bin/env python

import os
import shlex
import subprocess
from subprocess import PIPE


def run_case(model, case):
    try:
        cmd = "mpirun -n 3 %s %s" % (model, case)
        print("Launching: \n %s" % cmd)
        process = subprocess.run(
            cmd,
            # shlex.split(cmd),  # make list from string
            stdin=PIPE, stdout=PIPE, stderr=PIPE, check=True, shell=True)

        stdout = process.stdout.decode()
        print("process return code: %s" % str(process.returncode))
        print(stdout)
        print(process.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(" --- Error --- ")
        print(str(e))
        print(str(e.stdout.decode()))
        print(str(e.stderr.decode()))
        print(" --- End of Error --- ")


path_to_tclb = "~/my_GIT/TCLB"
model_to_run = os.path.join(path_to_tclb, "CLB/d2q9_pf_cm/main")
path_to_case = os.path.join(path_to_tclb, "moje/python/case_operations/sample_case.xml")


run_case(model_to_run, path_to_case)
print(" --- End --- ")
