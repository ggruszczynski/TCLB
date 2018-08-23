
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
                          "Viscosity_l": None,
                          "VelocityX": None}

log_files = glob.glob(os.path.join(input_dir, '*.out'))

# Open output file in 'append' mode
with open(output_filename, "a", newline='') as out_file:
    writer = csv.writer(out_file, delimiter='\t',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(list(quantities_of_interest.keys()))

    for input_filepath in log_files:
        print("Analyzing %s" % input_filepath)

        # Open input file in 'read' mode
        with open(input_filepath, "r") as in_file:
            content = in_file.read()

            head, tail = os.path.split(input_filepath)
            quantities_of_interest["Job_No"] = tail

            quantities_of_interest["stopped_by_NaN"] = False
            if line_regex.search(content):
                quantities_of_interest["stopped_by_NaN"] = True

            for quantity in quantities_of_interest:
                for line in str.splitlines(content):
                    settings = re.findall("Setting %s" % quantity, line)
                    if settings:
                        number = re.findall("\([0-9]*[.][0-9]*\)", line)[0]
                        number = re.sub("\(", '', number)
                        number = re.sub("\)", '', number)
                        number = float(number)
                        quantities_of_interest[quantity] = float(number)

            writer.writerow(list(quantities_of_interest.values()))

print("\n\nwriting result to %s" % output_filename)
print("DONE")

data = pd.read_csv(os.path.join(output_filename), delimiter="\t")


filtered_data = data[(data.VelocityX == 0.01) & (data.stopped_by_NaN == False)]
density_ratio = filtered_data['Density_h'] / filtered_data['Density_l']
viscosity_ratio = filtered_data['Viscosity_h'] / filtered_data['Viscosity_l']

## make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
plt.plot(density_ratio, viscosity_ratio,  color="red",  marker=".", linestyle="", label=r'current model')
# plt.plot(np.arange(n)*1E3, mrt_ux_std, color="blue", marker="", linestyle="--", label=r'MRT')
# plt.plot(line_size, theoretical, color="black", marker="x", linestyle="", label='theoretical')

axes = plt.gca()
# axes.set_xlim([0,0.5*1E6])
# axes.set_ylim([0, 1.0])

# plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.ylabel(r'$\nu^*$')
plt.xlabel(r'$\rho^*$')

plt.title(r'Stability')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('Stability.png')
# fig.savefig('sigma_ux_rho%s_v%s_Ux%s.png' % (rho_ratio, v, Ux))
plt.show()

# plt.close(fig) # close the figure



# is_crashed = data["stopped_by_NaN"]
# df.query('(a < b) & (b < c)')
# df[(df.a < df.b) & (df.b < df.c)]


# d = {
#     'Name': ['Alisa', 'Bobby', 'jodha', 'jack', 'raghu', 'Cathrine',
#              'Alisa', 'Bobby', 'kumar', 'Alisa', 'Alex', 'Cathrine'],
#     'Age': [26, 24, 23, 22, 23, 24, 26, 24, 22, 23, 24, 24],
#
#     'Score': [85, 63, 55, 74, 31, 77, 85, 63, 42, 62, 89, 77]}
#
# df = pd.DataFrame(d, columns=['Name', 'Age', 'Score'])

# df.loc[df['Score'].idxmax()]