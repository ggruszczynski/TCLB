
import matplotlib.pyplot as plt
import numpy as np

import glob, os
import re
import csv


# Regex used to match relevant loglines (in this case, a specific IP address)
line_regex = re.compile(r"Stopping due to Nan value")


# Output file, where the matched loglines will be copied to
output_filename = os.path.normpath("output/parsed_lines.log")
# Overwrites the file, ensure we're starting out with a blank file
with open(output_filename, "w") as out_file:
    out_file.write("")

input_dir = "logs_to_analyze"

quantities_of_interest = {"stopped_by_NaN": None,
                          "Job_No": None,
                          "Density_h": None,
                          "Density_l": None,
                          "Viscosity_h": None,
                          "Viscosity_l": None}

log_files = glob.glob(os.path.join(input_dir, '*.out'))

# Open output file in 'append' mode
with open(output_filename, "a", newline='') as out_file:
    writer = csv.writer(out_file, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(list(quantities_of_interest.keys()))

    for input_filepath in log_files:
        print("Analyzing %s" % input_filepath)

        # Open input file in 'read' mode
        with open(input_filepath, "r") as in_file:
            content = in_file.read()

            quantities_of_interest["Job_No"] = input_filepath

            quantities_of_interest["stopped_by_NaN"] = False
            if line_regex.search(content):
                quantities_of_interest["stopped_by_NaN"] = True

            for quantity in quantities_of_interest:
                for line in str.splitlines(content):
                    settings = re.findall("Setting %s to " % quantity, line)
                    if settings:
                        number = re.findall("\([A-Z0-9]*.[0-9]*\)", line)[0]
                        number = re.sub("\(", '', number)
                        number = re.sub("\)", '', number)
                        number = float(number)
                        quantities_of_interest[quantity] = float(number)

            writer.writerow(list(quantities_of_interest.values()))

print("DONE")
