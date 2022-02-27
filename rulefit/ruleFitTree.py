import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# https://github.com/christophM/rulefit, has information for advantages and disadvantages
# https://machinelearningmastery.com/different-results-each-time-in-machine-learning/, different results each time
# About lasso regressions: https://www.statisticshowto.com/lasso-regression/
from rulefit import RuleFit

# coefficient (a) is the weight of the decision rule in the lasso regression
# support (s) is the percentage of data points to which the decision rule applies
# importance (I) is a function of the coefficient and support
# I = abs(a) * sqrt(s*(1-s))

# the number of conditions per decision rule limited to a depth of 3

# TRAINING THE MODEL

training = pd.read_csv("states.csv") # load data frame

y = training.cost_per_mbps.values # set y as label values
X = training.drop("cost_per_mbps", axis = 1)  # set x as feature values
X = X.drop("state", axis = 1)  # remove states column
features = X.columns # set names of features

X = X.to_numpy() # convert training to numpy array

rf = RuleFit()
rf.fit(X, y, feature_names = features) # generate decision rules using training data

# CHECKING MODEL ON TRAINING DATA

predictions = rf.predict(X) # predict values
training['prediction'] = predictions # add predictions to dataframe

# store results in separate data frame and print
training_results = training[['state', 'cost_per_mbps', 'prediction']].copy()
print(training_results.head())

# calculate RSME
n = training[training.columns[0]].count() # number of rows
# sum errors
error_sum = 0
training = training.reset_index()  # make sure indexes pair with number of rows
for index, row in training.iterrows():
    error_sum += (row['cost_per_mbps'] - row['prediction'])/n
RSME = np.sqrt(error_sum)
print("RSME: ", RSME)
print()

# PRINTING RULES OF MODEL AND IMPORTANCE OF FEATURES

# get rules and write to txt file to inspect
rules = rf.get_rules()
rules = rules[rules.coef != 0].sort_values("importance", ascending=False) # remove rules where lasso weight is 0 and sort data frame
rules = rules.drop("type", axis = 1)  # remove type column (all values are "rule")
f = open("rules.txt", "w")
f.write(rules.to_string())
f.close()

# get the importances of features and print them
    # J = Ij + sum r(Ir/m)
    # J is the importance of the feature
    # Ij is the importance of the linear term of the feature
    # sum r is the sum of all decision rules in which the feature appears
    # Ir is the importance of each decision rule
    # m is the number of features present in that rule 
fi = rf.get_feature_importance() 
print(fi)

# MAKING PREDICTIONS WITH MODEL

predict = pd.read_csv("years.csv")
X = predict  # set x as feature values
X = X.drop("year", axis = 1)  # remove years column
features = X.columns # set names of features

X = X.to_numpy()
predictions = rf.predict(X) # predict values
predict['prediction'] = predictions # add predictions to dataframe

# graph results
years = predict['year'].to_numpy()

plt.figure(figsize=(8, 5))
plt.subplot(2, 1, 1)
plt.plot(years, predictions, color='blue', lw=3)
plt.show()