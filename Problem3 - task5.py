""" Problem3 - task5.py """

# Import of the pyomo module
import pyomo.environ as pyo

#import matplotlib
import matplotlib.pyplot as plt


# Creation of a Concrete Model
model = pyo.ConcreteModel()


''' PARAMETERS '''

# Production [MW]
Pmin = {'Coal': 0,   'Gas': 0 , 'Wind': 0 , 'Solar': 0}
Pmax = {'Coal': [120] * 24, 'Gas': [30] * 24,
        'Wind': [32, 51, 19, 25, 19, 4, 2, 1, 0, 0, 0, 0, 2, 4, 9, 1, 41, 32, 
                 14, 14, 19, 32, 32, 41] ,
        'Solar': [0, 0, 0, 0, 2, 5, 8, 10, 12, 15, 18, 22, 25, 28, 30, 30, 30, 
                  25,20, 15, 10, 5, 0, 0] }   

# Load [MW]
Pload =[30,20,20,30,50,80,100,140,120,100,90,80,70,80,120,160,220,200,180,160,
        120,100,80,40]

## to make the implementation of the cost functions and emission functions a 
## bit easier, by removing the need to write out the complete functions for 
## both of the generators in the objective function and emission constraint

# Cost functions [NOK/MWh]
a ={'Coal': 200, 'Gas': 500,'Wind': 800,'Solar': 1000 } 
b ={'Coal': 65 , 'Gas': 120  ,'Wind': 40 ,'Solar': 35}


''' SETS '''

# Set of generators
model.generators = pyo.Set(initialize =['Coal','Gas','Wind','Solar']) 

''' Periods '''
model.periods= pyo.Set(initialize=range(0,24))
''' VARIABLES '''

# Variables for power generation
model.generation = pyo.Var(model.generators, model.periods)



''' OBJECTIVE FUNCTION '''

## the objctive function is the sum of the cost function for both generators
## the cost functions are dependent on the variables for power generation
  
def objective_function(model):
    return sum(a[i] + b[i]*model.generation[i,j] 
               for i in model.generators 
               for j in model.periods) 
model.obj= pyo.Objective(rule=objective_function, sense=pyo.minimize)



''' CONSTRAINTS '''

# Constraint for power generation

## ensuring that the power generation is not less than the minimum power
## generation or exceeds maximum power generation

def power_generation(model,i,j):
    return pyo.inequality(Pmin[i], model.generation[i,j], Pmax[i][j])
model.power_generation = pyo.Constraint(model.generators,model.periods,
                                        rule = power_generation)


# Constraint for power balance

## ensuring that the power generated is equal to the load demand
## no uncovered load demand or a surplus of power

def power_balance(model,j):
        return sum(model.generation[i,j] for i in model.generators)==Pload[j]
model.power_balance = pyo.Constraint(model.periods,rule = power_balance)


''' SOLVER '''

opt = pyo.SolverFactory('gurobi')
results = opt.solve(model,tee=True) 
results.write(num=1)

# Prepare hourly generation values for plotting
# We need to populate a 2-dimensional list
G=[]
# make a sublist for every generator
for i,k in enumerate(model.generators):
    G.append([])
    # for every hour append the hourly production value of the generator
    for j in range(0,24):
        G[i].append(pyo.value(model.generation[model.generators.at(i+1),j]))

# Plot the results nicely

plt.stackplot(range(1,25), G, labels=model.generators)
plt.legend(loc='upper left')
plt.margins(0,0.05)
plt.xticks(range(1,24,2))
plt.yticks(range(0,240, 20))
plt.grid()
plt.xlabel('Hour')
plt.ylabel('Power [MW]')
plt.title('Production profile')
plt.savefig('plots/P3T5-PowerPlot.png', dpi=150)

#Also print the total generation of each plant
for i,k in enumerate(model.generators):
    print("Daily production from", k, sum(G[i]), "MWh")
# And total cost    
print("Minimum daily cost:", pyo.value(model.obj), "EUR")
