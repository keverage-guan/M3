#https://www.toptal.com/algorithms/mixed-integer-programming

from pulp import LpMinimize, LpProblem, LpMaximize, LpVariable

### set constants

B_low = 140
B_mid = 500
B_high = 2000

A_low = 23.49325202
A_mid = 0.6789549833
A_high = 0.003281288918

B = 399.2085357 #in Mbps
A = 1.21 #in square miles

#create problem and specify minimize or maximize
model = LpProblem ( name ="min -cell - towers ", sense = LpMinimize) 

# create problem variables with minimum possible values
n_low = LpVariable ( name =" n_low ", lowBound =0 , cat ='Integer')
n_mid = LpVariable ( name =" n_mid ", lowBound =0 , cat ='Integer')
n_high = LpVariable ( name =" n_high ", lowBound =0 , cat ='Integer')

# set constraints
model += ( A_low * n_low + A_mid * n_mid + A_high * n_high >= A )
model += ( B_low * n_low + B_mid * n_mid + B_high * n_high >= B )
model += ( A_low * B_low * n_low + A_mid * B_mid * n_mid + A_high * B_high * n_high >= A * B )

# set the objective function, i.e. the expression you want to minimize or maximize
obj_func = n_low + n_mid + n_high
model += obj_func


# solve the optimization problem and print results
status = model.solve()
# Print results
for var in model.variables () :
    print ( f"{var.name}: {int(var.value())}")