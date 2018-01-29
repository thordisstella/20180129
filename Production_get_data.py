'''
@author: Thordis Stella

This module is used to retrieve the data needed for this analysis. All the data is available online at www.data.cityofnewyork.us.
For further information, see https://dev.socrata.com/foundry/data.cityofnewyork.us/fhrw-4uyv and https://dev.socrata.com/foundry/data.cityofnewyork.us/27iv-9uub.
'''
from sodapy import Socrata
from Analysis import External_info
import pandas as pd

'''
--------------------------------- Initialization of necessary variables ---------------------------------------------------
To retrieve the necessary data from online we need to know the names, as defined on www.data.cityofnewyork.us, of that two datasets. 
The app_token, username and password are optional, but advisable. Here we have used log-in credentials created for this analysis.
'''
dataset_311_id="fhrw-4uyv"   
data_pop_id = "27iv-9uub"                                                          
app_token = 'hjud0ot8XxK9PvVzqLx5pKIec'
username = External_info.username
password = External_info.password
'''
--------------------------------- Functions to retrieve data for analysis -------------------------------------------------
'''
# This function returns the number of service requests that the NYPD received per borough and month during the provided year. year needs to be inclusively between 2010 and the present year.
# The returned object is a DataFrame.
# The open-source data that is retrieved here is available at https://dev.socrata.com/foundry/data.cityofnewyork.us/fhrw-4uyv. 
def get_311_NYPD_data(year):
    client = Socrata("data.cityofnewyork.us"                  # This creates a list of dictionaries (Python representation of a json object)
            , app_token
            , username=username
            , password=password)
    select_string = "select agency, date_extract_y(created_date) as year_created, date_extract_m(created_date) as month_created, borough, count(unique_key) as num_reqs where agency = 'NYPD' and year_created="+"'{}'".format(year)+" and borough != 'Unspecified' group by month_created, agency, borough, year_created limit 100"
    result = client.get(dataset_311_id,query=select_string)
    for row in range(len(result)):
        result[row]['num_reqs']=float(result[row]['num_reqs'])
    return pd.DataFrame.from_records(result)

# This function returns the population per borough in New York. The returned object is a DataFrame.
# The open-source data that is retrieved here is available at https://dev.socrata.com/foundry/data.cityofnewyork.us/27iv-9uub. 
def get_population_data():
    client = Socrata("data.cityofnewyork.us"
            , app_token
            , username=username
            , password=password) 
    result = client.get("27iv-9uub", limit=2000)
    return pd.DataFrame.from_records(result)