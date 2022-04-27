""" Problem3 - task2 sensitivity.py """

# Import of the pyomo module
import pyomo.environ as pyo

#import matplotlib
import matplotlib.pyplot as plt


# Creation of a Concrete Model
model = pyo.ConcreteModel()


''' PARAMETERS '''

# Production [MW]
Pmin = {'Coal': 0,   'Gas': 0 , 'Wind': 0 , 'Solar': 0}
Pmax = {'Coal': 120, 'Gas': 30, 'Wind': 50 ,'Solar': 30 }   

# Load [MW]
Pload =[30,20,20,30,50,80,100,140,120,100,90,80,70,80,120,160,220,200,180,160,
        120,100,80,40]

## to make the implementation of the cost functions and emission functions a 
## bit easier, by removing the need to write out the complete functions for 
## both of the generators in the objective function and emission constraint

# Cost functions [NOK/MWh]
a ={'Coal': 200, 'Gas': 500,'Wind': 800,'Solar': 1000 } 
b ={'Coal': 60 , 'Gas': 100  ,'Wind': 120 ,'Solar': 150}
#b Part B
#b ={'Coal': 65 , 'Gas': 120  ,'Wind': 40 ,'Solar': 35}

'Task 2'
#Emision CO2
e_co2 = {'Coal': 1.5, 'Gas': 0.2,'Wind': 0,'Solar': 0 } 



''' SETS '''

# Set of generators
model.generators = pyo.Set(initialize =['Coal','Gas','Wind','Solar'])

# Set of periods
model.periods= pyo.Set(initialize=range(0,24))


''' VARIABLES '''

# Variables for power generation
model.generation = pyo.Var(model.generators, model.periods)

''' CONSTRAINTS '''

# Constraint for power generation

## ensuring that the power generation is not less than the minimum power
## generation or exceeds maximum power generation

def power_generation(model,i,j):
    return pyo.inequality(Pmin[i], model.generation[i,j], Pmax[i])
model.power_generation = pyo.Constraint(model.generators,model.periods,
                                        rule = power_generation)


# Constraint for power balance

## ensuring that the power generated is equal to the load demand
## no uncovered load demand or a surplus of power

def power_balance(model,j):
        return sum(model.generation[i,j] for i in model.generators)==Pload[j]
model.power_balance = pyo.Constraint(model.periods,rule = power_balance)


## Returns the optimal daily cost for a given CO2 cost
def min_cost(cost_e_co2):
    ''' OBJECTIVE FUNCTION '''
    
    model.del_component('obj') # cleanup before changing parameters
    
    ## the objctive function is the sum of the cost function for both generators
    ## the cost functions are dependent on the variables for power generation
    ## as well as emission and emission tax
    def objective_function(model):
        return sum(a[i] + b[i]*model.generation[i,j] 
                   + e_co2[i]*cost_e_co2*model.generation[i,j]
                   for i in model.generators 
                   for j in model.periods) 
    model.obj= pyo.Objective(rule=objective_function, sense=pyo.minimize)

    ''' SOLVER '''
    
    opt = pyo.SolverFactory('gurobi')
    opt.solve(model,tee=True) 
    
    return pyo.value(model.obj)

# Run the optimizer and list the results for each CO2 cost
O_cost_e = []
for i in range(10,150, 20):
    O_cost_e.append(min_cost(i))

# Plot the sensitivity analysis
plt.plot(range(10,150, 20), O_cost_e)
plt.margins(0,0.05)
plt.gcf().subplots_adjust(left=0.15)
plt.xticks(range(10,150,20))
plt.yticks(range(250000,450000, 25000))
plt.xlabel('Carbon tax [EUR/tonCO2]')
plt.ylabel('Cost [EUR]')
plt.title('Sensitivity of optimal cost to carbon tax')
plt.grid()
plt.savefig('plots/P3T2Sensitivity.png', dpi=150)

