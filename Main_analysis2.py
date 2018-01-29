'''
@author: Thordis Stella
'''
import pandas as pd
from sodapy import Socrata
from Analysis import Helper_functions, External_info    


'''
------------------------- Set up a connection ----------------------------
'''
dataset_id="fhrw-4uyv"
app_token = 'hjud0ot8XxK9PvVzqLx5pKIec'
username = External_info.username
password = External_info.password

client = Socrata("data.cityofnewyork.us"
                  , app_token
                  , username=username
                  , password=password)

'''
------------------------- Get familiar with raw data ----------------------------------
Here we load 5 rows from the dataset into memory to get an idea about what the data looks like
'''
sample_data = client.get(dataset_id, limit=5)
sample_data_df = pd.DataFrame.from_records(sample_data)
print("Below we can see examples of rows from the data.")
print(sample_data_df.head())
print("")

print("Following is a list of the names of columns in the data:")
for key, value in sample_data[0].items():
    print(key)
print("")
    
'''
----------------- Basic analysis to better understand the data ----------------------------
'''
complaints_year_borough = Helper_functions.page_through_data(client, dataset_id, 10000, select="date_extract_y(created_date)as year, borough, complaint_type, unique_key", limit=1000000, group_by=["year","borough","complaint_type"])
print(complaints_year_borough)
    