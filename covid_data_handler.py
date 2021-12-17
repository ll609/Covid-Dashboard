import csv
from uk_covid19 import Cov19API
import logging
import pandas as pd
import sched, time
from config_handler import config_handler

def parse_csv_data(csv_filename: str) -> str:
    with open(csv_filename, 'r', newline='\n') as f:
        logging.info(f'CSV file opened: {csv_filename}')
        reader = csv.reader(f)
        logging.info(f'CSV file read: {csv_filename}')
        '''Opens the csv file using its file name, and splits the lines where there are new 
        lines. The file is read using the csv module to get it in the correct format'''
        rows = list(reader) #Converts into a usable data structure
        logging.info(f'CSV file converted into list: {csv_filename}')
        return rows

def process_covid_csv_data(covid_csv_data: list[list[str]]) -> tuple:
    cases = 0
    if covid_csv_data[1][-2]:
        hospital_cases = int(float(covid_csv_data[1][-2]))
        logging.info(f'Hospital cases found and set on second row: {hospital_cases}')
        #The nations_2021-10-28.csv file's data starts on the second line
    elif covid_csv_data[2][-2]:
        hospital_cases = int(float(covid_csv_data[2][-2]))
        logging.info(f'Hospital cases found and set on third row: {hospital_cases}')
        '''The Cov19API's doesn't include hospital data on the most recent day, so instead
        checks the line below'''
    else:
        hospital_cases = 'Null'
        logging.warning(f'Hospital cases not found and set to Null')
        '''For certain locations, there are no hospital cases data so therefore returns Null
        to show this. If the above statements are False, there are likely no hospital cases for
        the rest of the dataset, and if so, they won't be very useful as they are outdated'''
    i = 1
    exist = False
    while not exist:
        if covid_csv_data[i][-3] == '':
            i = i + 1
        else:
            exist = True
    if exist == True:
        cum_no_deaths = int(float(covid_csv_data[i][-3]))
        logging.info(f'Cumulative number of deaths found on row {i}')
    else:
        cum_no_deaths = 'Null'
        logging.warning(f'Cumulative number of deaths not found and set to Null')
    '''The third column from the right contains the cumulative deaths data. In the case of the 
    nation_2021-10-28.csv file, this data is missing for the most recent days so it checks the 
    rows until there is data present'''
    for j in range(3, 10):  
        cases += int(float(covid_csv_data[j][-1]))
    logging.info(f'Number of cases in last 7 days calculated: {cases}')
    #The number of cases of the last 7 days are counted from the week 2 days before

    return cases, hospital_cases, cum_no_deaths

def covid_API_request(location:str ='Exeter', location_type:str ='ltla') -> str:
    location_filter = [f'areaType={location_type}', f'areaName={location}']
    logging.info(f'Location filter set for Covid API: {location_filter}')
    '''This selects the appropriate location (such as a city or country) and location type (local
    or national) to display relevant data. The default location is Exeter if no arguments are
    entered'''
    cases_and_deaths = {"areaCode": "areaCode", "areaName": "areaName", "areaType": "areaType", 
    "date": "date", "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate", 
    "hospitalCases": "hospitalCases", "newCasesBySpecimenDate": "newCasesBySpecimenDate"}
    logging.info(f'Columns set for Covid API: {cases_and_deaths}')
    #Specifies the data of interest and the order this should come in
    
    api = Cov19API(filters=location_filter, structure=cases_and_deaths)
    logging.info('Location filter and columns set for API')
    data = api.get_json()
    logging.info('API retrieved as a dictionary by JSON')
    '''Retrieves the data of interest for the specified location from the API. Using JSON, the
    request is read as a dictionary, a usable data structure'''
    return data

def dict_to_csv(data: dict) -> str:
    df = pd.DataFrame.from_dict(data['data'])
    logging.info('API covid data stored in dataframe')
    file = config_handler()[1]
    logging.info(f'CSV file retrieved to write into: {file}')
    df.to_csv(file, index=None)
    logging.info(f'API covid data written into file: {file}')
    '''The data is converted into a csv file so the operations in the process_covid_csv_data
    function will also work for this data'''
    return file

def schedule_covid_updates(update_interval: int, update_name: str, location: str='Exeter', location_type: str='ltla'):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(update_interval, 1, covid_API_request, (location, location_type))
    logging.debug('Covid update data scheduler set')
    '''Runs the scheduler, which calls the covid_API_request function with the appropriate arguments
    once the time in the update_interval variable is reached'''
    s.run(blocking=False)
    logging.debug('Covid update data scheduler running')
    #Runs the scheduler without holding up other operations in the program