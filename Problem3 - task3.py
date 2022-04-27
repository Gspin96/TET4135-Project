""" Problem3 - task3.py """

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

#Emision cost [EUR/ton CO2]
cost_e_co2 = 60

#Emission NOx [tons NOx / MWh)
E_nox = {'Coal': 0, 'Gas': 0.1,'Wind': 0,'Solar': 0 } 

# Maximum emission ton [NOx/day]
E_nox_max = 30


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
               + e_co2[i]*cost_e_co2*model.generation[i,j]
               for i in model.generators 
               for j in model.periods) 
model.obj= pyo.Objective(rule=objective_function, sense=pyo.minimize)



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


# Constraint for emission 

## ensuring that the total NOx emissions do not exceed the emission limit

def emission(model,i,j):
    return  sum(E_nox[i]*model.generation[i,j]
                for i in model.generators for j in model.periods)  <= E_nox_max
model.emission = pyo.Constraint(model.generators, model.periods, rule = emission)


''' SOLVER '''

opt = pyo.SolverFactory('gurobi')
results = opt.solve(model,tee=True) 
results.write(num=1)

print("Minimum daily cost:", pyo.value(model.obj), "EUR")

# Prepare hourly generation values for plotting
# We need to populate a 2-dimensional list
G=[]
# make a sublist for every generator
for i,k in enumerate(model.generators):
    G.append([])
    # for every hour append the hourly production value of the generator
    for j in range(0,24):
        G[i].append(pyo.value(model.generation[model.generators.at(i+1),j]))
        
#Plot the generation
plt.figure(0)
plt.stackplot(range(1,25), G, labels=model.generators)
plt.legend(loc='upper left')
plt.margins(0,0.05)
plt.xticks(range(1,24,2))
plt.yticks(range(0,240, 20))
plt.grid()
plt.xlabel('Hour')
plt.ylabel('Power [MW]')
plt.title('Production profile')
plt.savefig('plots/P3T3-PowerPlot.png', dpi=150)

# Prepare hourly CO2 emission for plotting
# We need to populate a list with the value for each our
CO2 = []
for j in range(0,24):
    #sum emission of all generators in the hour j
    CO2.append(sum(e_co2[i]*pyo.value(model.generation[i,j]) for i in model.generators))

plt.figure(1)
plt.plot(range(1,25), CO2)
plt.margins(0,0.05)
plt.xticks(range(1,24,2))
plt.yticks(range(0,200, 20))
plt.grid()
plt.xlabel('Hour')
plt.ylabel('CO2 [tons]')
plt.title('CO2 Emissions')
plt.savefig('plots/P3T3-CO2.png', dpi=150)

print("Total CO2 emission:", sum(CO2), "tons")

# Prepare hourly NOx emission for plotting
# We need to populate a list with the value for each our
nox = []
for j in range(0,24):
    #sum emission of all generators in the hour j
    nox.append(sum(E_nox[i]*pyo.value(model.generation[i,j]) for i in model.generators))

plt.figure(2)
plt.plot(range(1,25), nox)
plt.margins(0,0.05)
plt.xticks(range(1,24,2))
plt.grid()
plt.xlabel('Hour')
plt.ylabel('NOx [tons]')
plt.title('NOx Emissions')
plt.savefig('plots/P3T3-NOx.png', dpi=150)

print("Total NOx emission:", sum(nox), "tons")


