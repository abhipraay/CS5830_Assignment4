import pandas as pd
from zipfile import ZipFile
import os
import yaml

def data_processing():

    ## Retrieve path of current directory
    script_directory = os.path.dirname(__file__)

    ## Open the parameters yaml file to obtain file name and field name
    try:
        with open(script_directory+'/file_params.yaml', 'r') as file:
            parameters = yaml.safe_load(file)
    except Exception as e:
        print("Error encountered while reading the yaml file")

    ## Load the data into a dataframe
    data_frame = pd.read_csv(script_directory+'/'+parameters['file_name'])

    data_frame['DATE'] = pd.to_datetime(data_frame['DATE'])
    data_frame['Month'] = data_frame['DATE'].dt.month

    ## Compute the monthly average values by grouping the data by month
    monthly_averages = data_frame.groupby('Month')[parameters['field_name']].mean()

    try:
        ## Write the computed monthly values to a csv file
        monthly_averages.to_csv(script_directory+'/monthly_computed.csv', index=False)
    except Exception as e:
        print("Error encountered while writing to the csv file")

data_processing()
