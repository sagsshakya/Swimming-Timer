'''
Author: Sagun Shakya
Date: 26-07-2022
Day: Tuesday

Description
-----------
Parses a zip file that contains a folder which again contains txt files to at most 5 files that has the info regarding the total time and the lap duration.
Finally, it will convert the overall info into a dataframe such that:
    - Index: <names of the students>
    - Columns: [student_name	total_time	lap_1_duration	lap_1_cumulative	lap_2_duration	lap_2_cumulative	lap_3_duration	lap_3_cumulative]
'''

# Necessary imports.
import zipfile
import os
from datetime import datetime
import pandas as pd
from warnings import filterwarnings
filterwarnings(action = "ignore")

def parse_rawfile(config: dict): 
    """
    Parses a zip file that contains a folder which again contains txt files to at most 5 files that has the info regarding the total time and the lap duration.
    Finally, it will convert the overall info into a dataframe such that:
        - Index: <names of the students>
        - Columns: [student_name	total_time	lap_1_duration	lap_1_cumulative	lap_2_duration	lap_2_cumulative	lap_3_duration	lap_3_cumulative]
    """ 
      
    N_LAPS = config['n_laps']
    input_dir = config['input_dir']

    # Containers.
    collection = dict()
    df_coll = pd.DataFrame()

    # Select zip files.
    filelist = os.listdir(input_dir)
    group = [file for file in filelist if file.endswith('.zip')]
    if len(group) > 0:
        group_name = os.path.join(input_dir, group[0])

    archive = zipfile.ZipFile(group_name, 'r')

    # Retrieve name list.
    name_list = archive.namelist()

    # Extract a specific file from the zip container.
    for student in name_list:
        collection[student] = []
        f = archive.open(student, 'r')

        # Read the content (will output byte object at first).
        content = f.read()

        # Decode the byte to sting encoded in utf-8.
        content = content.decode("utf-8")

        # index of 'Open on your desktop:'.
        df = content.split("\n")
        unwanted_index = df.index('Open on your desktop:') - 1
        assert unwanted_index is not None

        # Total time is in the first row.
        total_time = df[0].split(":", maxsplit = 1)[-1]

        # To datetime.
        total_time = datetime.strptime(total_time, '%H:%M:%S.%f')

        # Store in dictionary.
        collection[student].append(("total_time", total_time.time()))

        # Store lap info in the dictionary.
        for data, lap in zip(df[2:], range(N_LAPS)):
            lap_duration, lap_cumulative = data.split(",")[1:]
            collection[student].append((f'lap_{lap+1}_duration', datetime.strptime(lap_duration.strip(), '%H:%M:%S.%f').time()))
            collection[student].append((f'lap_{lap+1}_cumulative', datetime.strptime(lap_cumulative.strip(), '%H:%M:%S.%f').time()))
        
        dff = pd.DataFrame(dict(collection[student]), index = [student[:-4]])
        assert len(dff) > 0, "dff is empty."
        
        # Append to master dataframe.
        df_coll = df_coll.append(dff)

    # Rename index.
    df_coll.index = [name.split("/")[-1].replace("_", "").title() for name in list(df_coll.index)]

    ## Prompt for the filename.
    filename = config['first_output_filename']
    if not filename.endswith(".tsv"):
        filename += ".tsv"

    # Save the output into a file.
    output_dir = config['output_dir']
    os.makedirs(output_dir, exist_ok = True)
    filename = os.path.join(output_dir, filename)
    df_coll.to_csv(filename, sep = '\t', index = True, header = True, index_label = 'student_name')

    print(f"...\nSuccessful!\nFile exported as: {filename}")