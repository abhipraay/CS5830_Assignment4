from sklearn.metrics import r2_score
import pandas as pd
import os

def evaluation():

    ## Retrieve path of current directory
    script_directory = os.path.dirname(__file__)

    try:
        ## Load the ground truth and computed monthly values
        monthly_values = pd.read_csv(script_directory+'/monthly_values.csv')
        monthly_values_computed = pd.read_csv(script_directory+'/monthly_computed.csv')
    except Exception as e:
        print("Error encountered while reading the csv files")

    ## If the length of the two datasets is not equal, truncate the longer dataset
    if len(monthly_values) != len(monthly_values_computed):
        if len(monthly_values) > len(monthly_values_computed):
            monthly_values = monthly_values[:len(monthly_values_computed)]
        else:
            monthly_values_computed = monthly_values_computed[:len(monthly_values)]

    ## Compute the R2 score
    r2 = r2_score(monthly_values, monthly_values_computed)

    ## Check if the dataset is consistent
    if r2 >= 0.9:
        print('The dataset is consistent')
    else:
        print('The dataset is not consistent')
    return r2

evaluation()
