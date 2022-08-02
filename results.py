'''
Author: Sagun Shakya
Date: 26-07-2022
Day: Tuesday

Description
-----------
Reads the TSV file which contains the processed data (output from parser.py) and sorts the rows according to their total times.
Invokes df2pdf function from utils to first convert the pandas dataframe into a matplotlib table and
finally exports it to a PDF.

Columns: ['Rank', "Students' Name", 'Time Elapsed'] 
'''

# Dependencies.
from os.path import join
from pandas import read_csv
from utils import df2pdf, get_rank

def generate_result(config: dict):
    """
    Reads the TSV file which contains the processed data (output from parser.py) and sorts the rows according to their total times.
    Invokes df2pdf function from utils to first convert the pandas dataframe into a matplotlib table and
    finally exports it to a PDF.

    Columns: ['Rank', "Students' Name", 'Time Elapsed'] 

    Args:
        config (dict): configuration dictionary from YAML file.
    """
    
    # Read the TSV file.
    # The TSV file is supposed to be stored in the output folder but can be changed later using a config file.
    filepath = join(config['output_dir'], config['first_output_filename'])      # 'output\sample.tsv'

    df = read_csv(filepath, delimiter = '\t', skip_blank_lines = True, encoding = 'utf8')
    df.set_index('student_name', drop = True, inplace = True)

    # Verbosity.
    print("Unsorted:\n", df.total_time)

    # Get the result and display it.
    result = get_rank(df['total_time'])
    print("\nSorted:\n", result)

    # Rename Columns.
    result.columns = ['Rank', "Students' Name", "Time Elapsed"]
        
    # Convert the result into a PDF.
    df2pdf(result, figsize = (12,8), save_location = config['output_dir'])