import os
import pandas as pd
from .visualisations import *

def save_csv(data, path, filename, index=False, force=True):
    """
    Helper-Function to export pandas DataFrames into `csv` format using pandas built-in method `to_csv()`. The function provides functionality to force the creation of the path if not previously located in the file structure.

    Parameters:
        data                : pd.DataFrame
        path                : str (relative path from directory of execution file)
        filename            : str (descriptive filename (NOTE: without `.csv` file extension))
        index               : boolean (Specifies saving process in pandas.to_csv(). For more information check out the documentation of `to_csv()`)
        force               : boolean (True for automatic path creation using `os`)
    Return:
        None
    """
    if force:
        try: os.makedirs(path)
        except: None
    data.to_csv(f"{path}{filename}.csv", index=index)

def save_numerical_report(summary, path, filename, force=True, save_to='csv'):
    """
    Function to save the SUMMARY['dataset_name`] dictionary into either `csv` or `json` format for further use or extensive inspection by specifying a having path and filename. 

    Parameters:
        summary         : dict (SUMMARY dict holding information about each column of the dataset)
        path            : str (Relative path to location of saving)
        filename        : str (Filename (without suffix `.csv` or `.json`))
        save_to         : str (either `csv` or `json`)
    Return: None 
    """
    summary_dataframe = pd.DataFrame(summary)
    
    if force:
        try: os.makedirs(path)
        except: None

    if save_to == 'csv': summary_dataframe.to_csv(f'{path}/summary_{filename}.csv')
    elif save_to == 'json': summary_dataframe.to_json(f'{path}/summary_{filename}.json')
    else: raise NameError(f"'{save_to}' not defined. Try saving to 'csv' or 'json' format.")
    print(f"Saved: {filename}.{save_to} to {path}")

def save_figure(figure, path, filename, force=True, save_to='pdf'):
    """
    Function to save any matplotlib figure into a specified (relative) path and given filename. The function provides functionality to force the creation of the path if not previously located in the file structure.

    Parameters:
        figure          : plt.Figure 
        path            : str (Relative path to location of saving)
        filename        : str (Filename (without suffix `.csv` or `.json`))
        force           : boolean (Creates Path automatically if `True`, else `False`)
        save_to         : str (either `csv` or `json`)
    Return: None 
    """
    if force:
        try: os.makedirs(path)
        except: None

    figure.savefig(f'{path}/{filename}.{save_to}')
    print(f"Saved: '{filename}.{save_to}' to {path}")

def save_all_single_variable_analysis(summary, path, missing_values=False):
    """
    Function to save all figures from the single variable analysis automatically into a specified (relative) path. Filenames are generated automatically. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline plotting

    Parameter:
        summary             : dict (central data structure to hold information about all columns in dataset)
        path                : str (Relative path to location of saving)
        keep_missing_values : boolean (plot with or without missing values)
    Return: 
        fig                 : matplotlib.Figure 
    """
    for column in range(len(summary)):
        if summary[column]['Plot'] == 'bar':
            # create barplot
            fig = barplot(summary[column], keep_missing_values=missing_values)

            # set path to save to 
            if missing_values: spath = path + 'with_missing_values'
            else: spath = path + 'without_missing_values'

            # save to path
            save_figure(fig, spath, filename=f"{column}_{summary[column]['Name']}", save_to='pdf')

        elif summary[column]['Plot'] == 'hist':
            # create histogram
            fig = histogram(summary[column], keep_missing_values=missing_values)

            # set path to save to 
            if missing_values: spath = path + 'with_missing_values'
            else: spath = path + 'without_missing_values'

            save_figure(fig, spath, filename=f"{column}_{summary[column]['Name']}", save_to='pdf')

        if summary[column]['Summary']:
            # create boxplot
            fig = boxplot(summary[column])

            # set path to save to 
            spath = path + 'boxplots'
            
            save_figure(fig, spath, filename=f"{column}_{summary[column]['Name']}", save_to='pdf')

def save_all_categorical_scatters(data, summary, severity, path):
    """
    Function to save all categorical scatters for a given dataset automatically into a specified (relative) path. Filenames are generated automatically. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline     plotting

    Parameter:
        data                : pd.DataFrame (whole dataset)
        summary             : dict (central data structure to hold information about all columns in dataset)
        path                : str (Relative path to location of saving)
        keep_missing_values : boolean (plot with or without missing values)
    """
    for i in range(len(summary)):
        if summary[i]['Plot'] == 'hist':
                fig = categorical_scatterplot(summary[6], severity, summary[i], data.iloc[:,i], _exclude=0, _kind='svarm') # catch errors when scatter cannot be computed

                spath = path 
                save_figure(fig, spath, filename=f"scatter_{i}_{summary[i]['Name']}", save_to='pdf')

def save_all_categorical_associations(data, severity_summary, dataset_name, summary, severity, path):
    """
    Function to save all association plots between two categorical variables for a given dataset automatically into a specified (relative) path. Filenames are generated automatically. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline     plotting

    Parameter:
        data                : pd.DataFrame (whole dataset)
        summary             : dict (central data structure to hold information about all columns in dataset)
        path                : str (Relative path to location of saving)
        dataset_name        : str (Identifier for dataset)
    """
    for i in range(len(summary)):
            try: 
                if summary[i]['Map']: # local authority highway and local authority district 
                    fig, V = categorical_association_test(data, severity_summary[6], severity, summary[i], data.iloc[:,i])

                    spath = path 
                    save_figure(fig, spath, filename=f"chi2_{V}_{i}_{summary[i]['Name']}", save_to='pdf')
            except: None

# save_all_categorical_associations(data = DATA_LEEDS[dataset], severity_summary=SUMMARY['accidents'][6], dataset_name=dataset, summary=SUMMARY[dataset], severity= SEVERITY[dataset], path=PATH['reports']['leeds'] + PATH[dataset] + 'associations/')

def save_map(_map, path, filename):
    """
    Function to save a `folium.Map` object in `html` format into the specified (relative) path with the given filename.

    Parameters:
        _map        : folium.Map
        path        : str (Representing relative path to save location)
        filename    : str 
    """
    try:
        os.makedirs(path)
    except: None

    _map.save(f'{path}/{filename}.html')