import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
import yaml

## Retrieve path of current directory
script_directory = os.path.dirname(__file__)

## Set path of the config file
yaml_file = os.path.join(script_directory, 'config.yaml')

## Extract data from the config yaml file
try:
    with open(yaml_file, 'r') as yaml_file:
        parameters = yaml.safe_load(yaml_file)
except Exception as e:
   print("Error encountered while reading the config file")

year = parameters['year']
url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}/'

## Send API call to the URL
response = requests.get(url)

## Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')
rows = soup.find("table").find_all("tr")[2:-2]

file_names = []

total = parameters.get('n_locs')

## Extract data and file names
for i in range(total):
    index = random.randint(0, len(rows))
    data = rows[index].find_all("td")
    file_names.append(data[0].text)

## Write the data to the files
for name in file_names:
    new_url = url + name
    response = requests.get(new_url)
    open(name,'wb').write(response.content)

## Zip the files
try:
    with ZipFile(os.path.join(script_directory, '/zipped_weather.zip'),'w') as zip_file:
        for file in file_names:
            zip_file.write(file)
except Exception as e:
   print("Error encountered while zipping files")
    