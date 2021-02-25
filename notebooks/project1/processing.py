def check_indexes_in_subset(sub_dataset_indexes, main_dataset_indexes):
    """ 
    Helper-Function to evaluate whether there are indexes in the two linked sub datasets that do not appear in the main dataset.

    Parameters:
        sub_dataset_indexes         : pd.DataFrame
        main_dataset_indexes        : pd.DataFrame
    Return:
        #Wrong Indexes              : int (None if len() == 0)
    """
    assert len(main_dataset_indexes.shape) == 1 and len(sub_dataset_indexes.shape) == 1, 'Both function arguments must be one-dimensional'

    accidents_indexes = set(main_dataset_indexes)
    wrong_indexes = [i for i in set(sub_dataset_indexes) if i not in accidents_indexes]

    if len(wrong_indexes) == 0:
        return None
    else:
        return len(wrong_indexes)

def check_columns_for_missing_values(data):
    """
    For a dataset provided as a pd.DataFrame the function returns an informative string about each column containing null values, namely the number of missing values, the column index and the variable name of the column.

    Parameters:
        data                : pd.DataFrame
    Return:
        Informative String for each column containing null values, else None
    """
    for column in range(data.shape[1]):
        if sum(data.iloc[:,column].isnull()) != 0:
            print(f'{sum(data.iloc[:,column].isnull())} ({data.columns[column]}({column}))')