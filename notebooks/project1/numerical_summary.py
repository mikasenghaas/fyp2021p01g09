import numpy as np

def get_uniques_and_counts(data):
    """
    Helper-Function to return the uniques and their corresponding counts for a one-dimensional array/ vector or list of numbers using numpy's              'np.unique' method. 

    Parameter: 
        data        : pd.DataFrame / np.array (one-dimensional)
    Return:
        uniques     : np.array (one-dimensional)
        counts      : np.array (one-dimensional)
    """
    assert len(data.shape) == 1, 'Data must be one-dimensional.'
    uniques, counts = np.unique(data, return_counts=True)

    return uniques, counts

def get_fivenumsummary(data):
    """
    Helper-Function to return a five-number summary for a one dimensional array/ dataframe (column) using numpy's `np.percentile` function. This function restricts the input to only values greater than or equal to 0, in order to disregard missing values (`-1`)

    Parameter: 
        data                : pd.DataFrame / np.array (one-dimensional)
    Return:
        np.percentile()     : np.array (one-dimensional)
    """
    try: fivenum = np.percentile(data[data >= 0], [0, 25, 50, 75, 100])
    except: fivenum = None
    return fivenum

def compute_numerical_summary(summary, data): #
    for column in range(len(summary)):
        # compute number of uniques and counts for every column
        uniques, counts = get_uniques_and_counts(data.iloc[:,column])
        summary[column]['No_Uniques'] = len(uniques) # attach number of uniques for each column to SUMMARY
            
        # compute five-number summary if specified
        if summary[column]['Summary'] == True:
            summary[column]['Five_Number_Summary'] = get_fivenumsummary(data.iloc[:,column])

        # attach uniques/ counts as dictionary for all variables that we want to plot as a barplot
        if summary[column]['Plot'] == 'bar': 
            if len(uniques) < 100:
                summary[column]['Uniques'] = {uniques[i]: counts[i] for i in range(len(uniques))}
        
        # attach data of the column for all variables that we want to plot as a histogram or need a five-number-summary
        if summary[column]['Plot'] == 'hist' or summary[column]['Summary'] == True:
            summary[column]['Data'] = np.array(data[summary[column]['Name']])