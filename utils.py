from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def get_rank(df: pd.DataFrame) -> pd.Series:
    """
    Gets the sorted Pandas Series; sorted as per the datetime format %H:%M:%S.%f.
    Sorted in Ascending order.
    Attaches the rank of the student, name of the student at the front columns.

    Args:
        df (pd.DataFrame): DataFrame containing the objects (string). e.g "00:09:60.1400"

    Returns:
        pd.Series: Sorted Series
    """
    df = df.apply(lambda x: datetime.strptime(x.strip(), '%H:%M:%S.%f').time())
    
    # Sort the values according to time and Take out the names of the students from the index column.
    df = df.sort_values(ascending = True).reset_index()
    
    # Attach the rank at the front.
    df = pd.concat([pd.DataFrame({"Rank" : [make_ordinal(ii+1) for ii in range(len(df))]}), df], axis = 1)
    
    return df

    
def df2pdf(df: pd.DataFrame, figsize: tuple = (10,2), save_location: str = 'output') -> None:
    """
    Converts the given dataframe into a matplotlib table and then exports it into a PDF.

    Args:
        df (pd.DataFrame): dataframe (target).
        figsize (tuple, optional): dimensions of the figure. Defaults to (10,2).
        save_location (str, optional): path to save folder. Defaults to 'output'.
    """
    num_cols = df.shape[1]
    COLORS = [['lightskyblue']*num_cols, ['palegreen']*num_cols, ['khaki']*num_cols, ['plum']*num_cols, ['lightsteelblue']*num_cols]
    
    fig, ax = plt.subplots(figsize = figsize)
    ax.axis('tight')
    ax.axis('off')
    ax.patch.set_facecolor('tab:cyan')
    
    # Titles.
    plt.suptitle("Swostishree Gurukul", fontsize = 30)
    ax.set_title("Results of Swimming Competition", fontdict = {'fontsize' : 20}, y = 1.0, pad = -16)
    
    # Create table.
    the_table = ax.table(cellText = df.values, 
                         colLabels = df.columns, 
                         loc = 'center', 
                         cellLoc = 'center', 
                         cellColours = COLORS)
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(16)
    the_table.alpha = 0.6
    
    # Set row height.
    for row_num in range(df.shape[0] + 1):
        for r in range(df.shape[1]):
            cell = the_table[row_num, r]
            cell.set_height(0.1)
        
    #plt.show()
    
    # Convert to PDF.
    filename = os.path.join(save_location, 'Results.pdf')
    pp = PdfPages(filename)
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

def make_ordinal(n: int) -> str:
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix