'''
@author: Thordis Stella
This module is meant for viewing data that has been retrieved by Production_get_data and analysed by Production_do_analysis
'''
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from Analysis import Production_do_analysis

[input, real, pred] = Production_do_analysis.perform_lin_reg_for_population()
sqr_err = mean_squared_error(real,pred)
print("Mean squared error is {}".format(sqr_err))

plt.scatter(input, real)
plt.plot(input, pred)

plt.xlabel("Normalized population in borough")
plt.ylabel("Normalized number NYPD service requests")
plt.title("Service requests by population size")
plt.show()
