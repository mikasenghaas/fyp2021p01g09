def check_indexes_in_subset(sub_dataset, _in):
    """ 
    Helper-Function to evaluate whether there are indexes in the two linked sub datasets that do not appear in the main dataset.

    Parameters:
        sub_dataset         : pd.DataFrame
        _in                 : pd.DataFrame
    Return:
        #Wrong Indexes      : int (None if len() == 0)
    """
    
    accidents_indexes = set(_in['Accident_Index'])
    wrong_indexes = [i for i in set(sub_dataset['Accident_Index']) if i not in accidents_indexes]

    if len(wrong_indexes) == 0:
        return None
    else:
        return len(wrong_indexes)


def check_all_columns(data):
    """
    For a dataset provided as a pd.DataFrame the function returns an informative string about each column containing null values,         namely the number of missing values, the column index and the variable name of the column.

    Parameters:
        data                : pd.DataFrame
    Return:
        Informative String for each column containing null values, else None
    """
    for column in range(data.shape[1]):
        if sum(data.iloc[:,column].isnull()) != 0:
            print(f'{sum(data.iloc[:,column].isnull())} ({data.columns[column]}({column}))')

def hello():
    print('Hey from Processing Functions')