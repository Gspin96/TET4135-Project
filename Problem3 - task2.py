#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 09:47:04 2021

@author: renateberge
"""

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
P =[30,20,20,30,50,80,100,140,120,100,90,80,70,80,120,160,220,200,180,160,120,100,80,40]
Pload={}
for i in range(1,25):
    Pload[i]=P[i-1]

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

''' SETS '''

# Set of generators
model.generators = pyo.Set(initialize =['Coal','Gas','Wind','Solar']) 

''' Periods '''
model.periods= pyo.Set(initialize=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
''' VARIABLES '''

# Variables for power generation
model.generation = pyo.Var(model.generators, model.periods)

''' OBJECTIVE FUNCTION '''

## the objctive function is the sum of the cost function for both generators
## the cost functions are dependent on the variables for power generation
  
def objective_function(model):
    return sum(a[i] + b[i]*model.generation[i,j] + e_co2[i]*cost_e_co2*model.generation[i,j]
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

## ensuring that the total emissions do not exceed the emission limit

# def emission(model):
#     return  sum(cost_em1[i] + cost_em2[i]*model.generation[i] 
#                 + cost_em3[i]*model.generation[i]**2 
#                 for i in model.generators)  <= Emax
# model.emission = pyo.Constraint( rule = emission)


''' SOLVER '''

model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
opt = pyo.SolverFactory('gurobi')
# setting higher solver precision prevents error when computing duals 
# in some cases
# opt.options['BarQCPConvTol'] = 1E-7 
results = opt.solve(model,tee=True) 
results.write(num=1)
#model.display()
#model.dual.display()


#To make plot
G=[]
for i,k in enumerate(model.generators):
    G.append([])
    for j in range(1,25):
        G[i].append(pyo.value(model.generation[model.generators.at(i+1),j]))
plt.figure(0)
plt.stackplot(range(1,25), G, labels=model.generators)
plt.legend(loc='upper left')
plt.margins(0,0.05)
plt.xticks(range(1,24,2))
plt.yticks(range(0,240, 20))
plt.grid()
plt.xlabel('Hour')
plt.ylabel('Cost [NOK]')
plt.title('Production profile')
plt.savefig('plots/P3T2-PowerPlot.png', dpi=150)

#Plot emissions
CO2 = []
for j in range(1,25):
    CO2.append(sum(e_co2[i]*pyo.value(model.generation[i,j]) for i in model.generators))

plt.figure(1)
plt.plot(range(1,25), CO2)
plt.margins(0,0.05)
plt.xticks(range(1,24,2))
plt.yticks(range(0,200, 20))
plt.grid()

print("Total emission:", sum(CO2), "tons")


