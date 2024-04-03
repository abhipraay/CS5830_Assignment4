import pandas as pd
from zipfile import ZipFile
import os

def data_preparation():

    ## Retrieve path of current directory
    script_directory = os.path.dirname(__file__)

    ## Extract the zip file
    try:
        with ZipFile(script_directory+'/weather.zip', 'r') as zip_object: 
            zip_object.extractall(path=script_directory) 
    except Exception as e:
        print("Error encountered while extracting the zip file")

    try:
        files = os.listdir(script_directory)
        files = [file for file in files if file.endswith('.csv')]
        print(files)
    except Exception as e:
        print("Error encountered while finding files in the directory")

    file_name = ''

    for file in files:
        data_frame = pd.read_csv(script_directory+'/'+file)

        ## Choose the file that has the required fields
        if data_frame['MonthlyDepartureFromNormalAverageTemperature'].isnull().sum() < len(data_frame['MonthlyDepartureFromNormalAverageTemperature']) and data_frame['DailyDepartureFromNormalAverageTemperature'].isnull().sum() < len(data_frame['DailyDepartureFromNormalAverageTemperature']):
            file_name = file 
            field_name = 'DailyDepartureFromNormalAverageTemperature'

            ## Write the file name and field name to a yaml file
            try:
                with open(script_directory+'/file_params.yaml', 'w') as yaml_file:
                    yaml_file.write(f'file_name: {file_name}\n')
                    yaml_file.write(f'field_name: {field_name}\n')
            except Exception as e:
                print("Error encountered while writing to the yaml file")

    if file_name != '':
        ## Extract the ground truth values for monthly aggregates
        monthly_values = data_frame['MonthlyDepartureFromNormalAverageTemperature']
        monthly_values.dropna(inplace=True)

        ## Write the monthly ground truth values to a csv file
        monthly_values.to_csv(script_directory+'/monthly_values.csv', index=False)
    else:
        print("No file with the required fields found")

data_preparation()