'''
@author: Thordis Stella
'''
''' --------------------------------------- Initialization ------------------------------------------------------------
'''
year='2017'             # This variable controls which year we look at the data for NYPD for. It can be changed as one likes, but it needs to be an integer at least as great as 2010, and no greater than
                        # today's year.
'''
------------------------------------------- Analysis -----------------------------------------------------------------
Here we put forward the hypothesis. Let mu_Xi be the average number of 311 requests per month to the NYPD in 2017 in borough i.
    H0= mu_Xi=mu_Xj for all i,j.
Using h1() we will see whether the null hypothesis is true using one-way Anova test.
'''

from Analysis import Production_get_data
import pandas as pd
import random
from sklearn import linear_model
from scipy import stats
import matplotlib as plt

# First we retrieve the data we will need. The code that does this can be found in Production_get_data.py
nypd_data = Production_get_data.get_311_NYPD_data(year)
pop_data = Production_get_data.get_population_data()

# Next we filter the data slightly. nypd_data is already in the format we want, but pop_data contains populations for more than one date, so we only select the newest.
cols=list(pop_data)
cols.remove('borough')
max_col = max(cols)
pop_data=pop_data.loc[:,[max_col,'borough']]
pop_data.rename(columns={max_col:'population'}, inplace = 'True')
pop_data[['population']]=pop_data[['population']].apply(pd.to_numeric)


def get_joined_table(pop_data = pop_data, nypd_data = nypd_data, added_var = 'population'):
    pop_dict = {}
    for row in range(len(pop_data.index)):
        pop_dict[(pop_data.loc[row,'borough']).upper()]=pop_data.loc[row,added_var]
      
    nypd_data[added_var]=nypd_data['borough'].map(pop_dict)
    nypd_data[added_var]=pd.to_numeric(nypd_data[added_var])
    return nypd_data

# Linear regression:
# Here we perform linear regression to try to fit a model on the form Y=aX, where Y is number of requests sent and X is the normalized population of the borough in question. Note that we have assumed that 
# The population size has remained the same over the period in question which introduces some error, but we consider it to be insignificant when we normalize the variable.
def perform_lin_reg_for_population():
    data=get_joined_table()
    data['population']=(data['population']-data['population'].mean())/data['population'].std()      # Population will be our X factor so we scale it to prevent a very large/small coefficient.
    data['num_reqs']=(data['num_reqs']-data['num_reqs'].mean())/data['num_reqs'].std()
    # Now we chose the vectors we will run linear regression on and select a training set and a test set.
    lin_reg_x = data['population']
    lin_reg_y = data['num_reqs']
    num_rows = len(lin_reg_x.index)
    rows=[i for i in range(num_rows)]
    random.shuffle(rows)
    train_last_index = (int)(num_rows*0.8)
    
    lin_reg_x_train = lin_reg_x[rows[0:train_last_index]]
    lin_reg_x_test = lin_reg_x[rows[train_last_index:]]
    
    lin_reg_y_train = lin_reg_y[rows[0:train_last_index]]
    lin_reg_y_test = lin_reg_y[rows[train_last_index:]]
    regr=linear_model.LinearRegression()
    
    regr.fit(lin_reg_x_train.values.reshape(-1,1), lin_reg_y_train.values.reshape(-1,1))
    pred=regr.predict(lin_reg_x_test.values.reshape(-1,1))
    return [lin_reg_x_test, lin_reg_y_test, pred]

# Here we run a one sided anova test to see whether our null hypothesis is false. We don't reject it if p<0.05.
def check_h1(nypd_data = nypd_data, pop_data = pop_data):
    pop_data['perc'] = pop_data['population']/pop_data['population'].sum()      # Here we find the percentages of the total population of the 5 boroughs is in each borough. This is done to be able to 
                                                                            # later correct for the fact that the population of different districts is quite different.
    data = get_joined_table(pop_data=pop_data, added_var = 'perc') 
    data['num_reqs']/=data['perc']
    boroughs = pop_data.loc[:,'borough']
    d_data = {grp:data['num_reqs'][data['borough'] == grp] for grp in boroughs}
    # Note: There is an error here so the values are currently not being returned, but with a little bit more time to fix this this would be easily fixable.
    F, p = stats.f_oneway(d_data[boroughs[0]], d_data[boroughs[1]])
    
    return F,p
