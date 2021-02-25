import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import textwrap

def initialise_summary(data, lookup, dataset_name, key, summary, labels, plotting, fivenum, start_at=0):
    """
    Function to initialise the central data structure SUMMARY for some information about the dataset.

    Parameters:
        dataset_name         : str (String identifying the dataset) 
        summary              : dict (Empty dict constants where to store the data (will be stored at key `dataset_name`))
        labels               : dict (dict holding the column indexes of the dataset at key `dataset_name`)
        plotting             : dict (dict holding the plotting behavior for each column at key `dataset_name`)
        fivenum              : dict (dict holding the column indexes of the dataset at key `dataset_name`)

    Returns:
        SUMMARY['dataset_name'] = {
            0: {'Name': <col_name>, 
                'Plot': <bar, hist, None>,
                'Summary': <True/False>,
                'Map': {...} (if available)},
            1: {...}
        }
    """

    # initialise the lookup dictionary with the column name and variable type
    summary[key] = {}
    for i in range(data.shape[1]):
        summary[key][i] = {'Name': list(data)[i]}
        if plotting[i] == 'bar':
            summary[key][i].update({'Plot': 'bar'})
        elif plotting[i] == 'hist':
            summary[key][i].update({'Plot': 'hist'})
        else: summary[key][i].update({'Plot': None})

        if i in fivenum:
            summary[key][i].update({'Summary': True})
        else: summary[key][i].update({'Summary': False})

    # add the maps to the lookup dictionary
    categorical_counter = 0
    for column in labels:
        if dataset_name == 'casualties':
            if categorical_counter == 2: 
                summary[key][column]['Map'] = lookup[35]
                categorical_counter += 1
                continue
            if categorical_counter == 10:
                summary[key][column]['Map'] = lookup[48]
                categorical_counter += 1
                continue
            if categorical_counter == 11:
                summary[key][column]['Map'] = lookup[47]
                categorical_counter += 1
                continue
        
        summary[key][column]['Map'] = lookup[start_at+categorical_counter]
        categorical_counter += 1

def barplot(summary, dimensions=(32,18), keep_missing_values=True):
    """
    Function to create barplot based on the SUMMARY data structure. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline plotting

    Parameter:
        summary             : dict (central data structure to hold information about all columns in dataset)
        dimensions          : tuple (specify size of plotted figure)
        keep_missing_values : boolean (plot with or without missing values)
    Return: 
        fig                 : matplotlib.Figure 
    """
    # create figure and axes (with padding for better exporting)
    fig = plt.figure(figsize=dimensions)
    ax = fig.add_axes([.15,.15,.7,.7]) # [left, bottom, width, height]
    
    # defining variables depending on missing_values variable
    if keep_missing_values:
        x = list(summary['Uniques'].keys())
        y = list(summary['Uniques'].values())
        title = title = f"Distribution: {summary['Name'].replace('_', ' ')} (with missing values)"
        color = 'darkred'
        yticks = list(summary['Uniques'].keys())
    
    else: 
        if -1 in list(summary['Uniques'].keys()):
            x = list(summary['Uniques'].keys())[1:]
            y = list(summary['Uniques'].values())[1:]
            yticks = list(summary['Uniques'].keys())[1:]
        else: 
            x = list(summary['Uniques'].keys())
            y = list(summary['Uniques'].values())
            yticks = list(summary['Uniques'].keys())

        title = f"Distribution: {summary['Name'].replace('_', ' ')} (without missing values)"
        color = 'darkblue'
        
    spaced_ticks = [i for i in range(len(yticks))]
    
    # plot 
    ax.barh(spaced_ticks, y, align='center', color=color)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Number of Accidents')
    try: # account for 0% datasets
        ax.set_xlim(0, 1.15*max(y)) 
    except: None

    ax.set_yticks(spaced_ticks)
    ax.tick_params(axis='y', which='major', pad=10)
    ax.invert_yaxis()

    try: 
        y_labels = [summary['Map'][i] for i in x] # use lookup from xls 
        if summary['Name'] == 'Number_of_Vehicles' or summary['Name'] == 'Number_of_Casualties': # account for weird textwrap behavior in these cols
            ax.set_yticklabels(y_labels)
        else: ax.set_yticklabels([textwrap.fill(label, 10) for label in y_labels]) # textwrap for nicer looking labelling
    except: None # account for variables that do not have lookup mapping

    # insert counts and percentages as text next to the corresponding bars
    for x_cord, y_cord in zip(spaced_ticks,y):
        ax.text(y_cord, x_cord, f'{y_cord} ({str(100*round(y_cord/sum(y), 3))[:5]}%)' , color='black', fontweight='bold')
    plt.tight_layout()

    return fig

def histogram(summary, dimensions=(32,18), keep_missing_values=True):
    """
    Function to create histogram based on the SUMMARY data structure. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline plotting

    Parameter:
        summary             : dict (central data structure to hold information about all columns in dataset)
        dimensions          : tuple (specify size of plotted figure)
        keep_missing_values : boolean (plot with or without missing values)
    Return: 
        fig                 : matplotlib.Figure 
    """
    assert summary['Plot'] == 'hist', "This variable cannot be plotted as a histogram. Check out the 'Plot' property in SUMMARY to see how to plot this attribute."

    # create figure and axes (with padding for better exporting)
    fig = plt.figure(figsize=dimensions)
    ax = fig.add_axes([.1,.1,.8,.8])

    # defining variables depending on missing_values variable
    if keep_missing_values:
        title = f"Distribution: {summary['Name'].replace('_', ' ')} (with missing values)"
        data = summary['Data']
        color = 'darkred'

    else: 
        title = f"Distribution: {summary['Name'].replace('_', ' ')} (without missing values)"
        data = summary['Data'][(summary['Data'] != -1)] # masking out -1
        color = 'darkblue'

    # plot
    ax.hist(data, bins=50, color=color)
    ax.set_title(title, fontweight='bold')
    ax.set_ylabel('Number of Accidents')
    ax.set_xlabel('Age')

    return fig

def boxplot(summary, dimensions=(16,9)):
    """
    Function to create a boxplot for numerical values based on the SUMMARY data structure. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline plotting

    Parameter:
        summary             : dict (central data structure to hold information about all columns in dataset)
        dimensions          : tuple (specify size of plotted figure)
        keep_missing_values : boolean (plot with or without missing values)
    Return: 
        fig                 : matplotlib.Figure 
    """
    assert summary['Summary']==True, "This variable does not require a five-number summary and can therefore not be plotted as a boxplot."

    # create figure and axes (with padding for better exporting)
    fig = plt.figure(figsize=dimensions)
    ax = fig.add_axes([.1,.1,.8,.8])

    # plot
    ax.boxplot(summary['Data']);
    ax.set_title(f"Boxplot of {summary['Name'].replace('_', ' ')}", fontweight='bold')

    return fig

def categorical_scatterplot(summary_categorical, data_categorical, summary_numerical, data_numerical, _kind='svarm', _exclude=100):
    """
    Function to create a categorical scatterplot (finding an association between a numerical and cateogrical variable) using `sns.catplot`. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline plotting

    Parameter:
        data                                  : pd.DataFrame (central data structure to hold information about all columns in dataset)
        summary_categorical_variable          : dict (SUMMARY of specific column)
        summary_numerical_variable            : dict (SUMMARY of specific column)
        _kind                                 : str (either 'svarm' or 'violin')
        _exclude                              : int (excludes plotting of attributes from the categorical variable that occur less than the specified value)
    Return: 
        fig                                   : matplotlib.Figure 
    """
    name_categorical, name_numerical = summary_categorical['Name'], summary_numerical['Name']
    data_categorical, data_numerical = data_categorical, data_numerical
    
    data_to_plot = np.array([data_categorical, data_numerical]).T
    
    # masking
    without_missing_values = (data_to_plot[:,0] > -1) & (data_to_plot[:,1] > -1) # we first mask out all data records where either of the two observed attributes has missing values

    uniques, counts = np.unique(data_categorical, return_counts=True)
    under_100 = [uniques[i] for i in range(len(counts)) if counts[i] < _exclude] # we then also mask out "irrelevant" 
    exclude_small_values = ~np.isin(data_categorical, under_100)

    final_mask = (without_missing_values) & (exclude_small_values)
    data_to_plot = data_to_plot[final_mask]
    
    if _kind == 'svarm':
        fig = sns.catplot(x = name_categorical, y = name_numerical, data=pd.DataFrame(data_to_plot, columns=[name_categorical, name_numerical]), kind='swarm', height=8.27, aspect=16/9, legend=True);
        try:
            fig.set_xticklabels([summary_categorical['Map'][i] for i in [j for j in uniques if j not in under_100]]);
        except: None
        fig.fig.suptitle(f'Categorical Scatterplot for {name_categorical.replace("_", " ")} and {name_numerical.replace("_", " ")}', fontweight='bold')
    elif _kind == 'violin':
        fig = sns.catplot(x = name_categorical, y = name_numerical, data=pd.DataFrame(data_to_plot, columns=[name_categorical, name_numerical]), kind='violin', height=8.27, aspect=16/9, legend=True);
        try:
            fig.set_xticklabels([summary_categorical['Map'][i] for i in [j for j in uniques if j not in under_100]]);
        except: None
        fig.fig.suptitle(f'Categorical Scatterplot for {name_categorical.replace("_", " ")} and {name_numerical.replace("_", " ")}', fontweight='bold')
    else: raise NameError(f"type = '{_kind}'' is not defined. Try 'svarm' or 'violin'")

    return fig;

def categorical_association_test(data, marker_variable_summary, marker_data, relational_variable_summary, relational_data):
    """
    Function to create an informative figure for evaluating the association of two categorical variables. Associativity Measure is based on Pearson Chi Squared Association Test using `sns.catplot`. Displays inline in Jupyter when called without additional parameters. Use %%capture to prevent inline plotting

    Parameter:
        data                                  : pd.DataFrame (central data structure to hold information about all columns in dataset)
        marker_variable_summary               : dict (SUMMARY of column for which we want to observe associativity)
        marker_data                           : np.array or pd.DataFrame
        relational_variable_summary           : dict (SUMMARY of related column)
    Return: 
        fig                                   : matplotlib.Figure 
        V                                     : float (Crawer's V [Value between [0,1] indicating the associativity])
    """
    name1, name2 = marker_variable_summary['Name'], relational_variable_summary['Name']
    data1, data2 = marker_data, relational_data

    #mask out missing data
    data_to_plot = np.array([data1, data2]).T
    
    # masking
    without_missing_values = (data_to_plot[:,0] > -1) & (data_to_plot[:,1] > -1) # we first mask out all data records where either of the two observed attributes has missing values
    data_to_plot = data_to_plot[without_missing_values]

    # crosstab
    observed_pd = pd.crosstab(data_to_plot[:,0], data_to_plot[:,1], rownames = [name1], colnames = [name2]).T
    observed = observed_pd.to_numpy()

    chiVal, pVal, df, expected = chi2_contingency(observed)
    chiVal, pVal, df, expected.astype(int)
    V = np.sqrt( (chiVal / observed.sum() ) / (min(observed.shape)-1) )

    fig, axes = plt.subplots(nrows=2, ncols=len(np.unique(data1)), figsize=(16, 9), constrained_layout=True)
    fig.suptitle(f"Association of {name1.replace('_', ' ')} and {name2.replace('_', ' ')} (chiVal: {round(chiVal, 2)}, pVal: {round(pVal, 2)}, V: {round(V, 2)})", fontweight='bold', fontsize=16)
    

    labels1 = [marker_variable_summary['Map'][i] for i in np.unique(data_to_plot[:,0])]
    labels2 = [relational_variable_summary['Map'][int(i)] for i in np.unique(data_to_plot[:,1])]
    x = np.array(labels2)

    for i, ax in enumerate(axes[0]):
        ax.plot(x, observed[:,i], 'ro-', label='Observed')
        ax.plot(x, expected[:,i], 'bo-', label='Expected')
        if i==0: 
            ax.set_ylabel('No. of Accidents')
            ax.legend(loc='best');
        ax.set_title(labels1[i])
        ax.set_xticks(x)

    for i, ax in enumerate(axes[1]):
        ax.plot(x, observed[:,i]/expected[:,i], 'go-')
        ax.plot(x, np.ones(x.shape), 'k:')
        
        if i==0: 
            ax.set_ylabel('Observed/Expected')
        ax.set_xticks(x)
        ax.set_xticklabels(labels2)
        fig.autofmt_xdate(rotation=45)
    
    return (fig, round(V,2))