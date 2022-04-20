# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:54:30 2022

@author: giova
"""

import math
from classes.Objects import Line

Plow = 1.25
Pmax_base = 3.5
Pchg = 0.055
Nchg = 52
disc_rate = 0.085

#High and low demand cost and hours per day

Cl = 210
Ch = 325
Th = 6
Tl = 24-Th

#Line characteristics:
U=10 #kV
Imax_25 = 0.255 #kA
L = 8
r = 18 #ohm*mm^2/km     resistivity

def problem1():
    print("\nProblem 1:")
    Pmax = Pmax_base + Pchg * Nchg    #MW
    Plim_25 = math.sqrt(3)*U*Imax_25  #MW

    print("Peak power: ",Pmax, " MW")
    print("Base line capacity: ", Plim_25, " MW")

def problem2():
    print("\nProblem 2:")
    Pmax = Pmax_base + Pchg * Nchg
    
    #Option 1: FeAl75 60mm^2 line
    FeAl75 = Line(U,r,L,60)
    FeAl75.calc_inv_annuity(750000, disc_rate, 20) #
    FeAl75.calc_op_cost(Plow, Pmax, Ch, Cl, Th)
    
    Wloss_y = (FeAl75.loss(Plow)*Tl + FeAl75.loss(Pmax)*Th)*365 #Yearly energy loss
    
    print("FeAl75 losses:")
    print("\tYearly: ", Wloss_y, " MWh")
    print("\to75: ", FeAl75.o, "NOK/y")
    print("\tf75: ", FeAl75.f, "NOK/y")
    print("\tc75: ", FeAl75.o + FeAl75.f, "NOK/y")
    
    #Option 2: FeAl90 90mm^2 line
    FeAl90 = Line(U,r,L,90)
    FeAl90.calc_inv_annuity(900000, disc_rate, 20)
    FeAl90.calc_op_cost(Plow, Pmax, Ch, Cl, Th)
    
    Wloss_y = (FeAl90.loss(Plow)*Tl + FeAl90.loss(Pmax)*Th)*365 #Yearly energy loss
    
    print("\nFeAl90 losses:")
    print("\tYearly: ", Wloss_y, " MWh")
    print("\to75: ", FeAl90.o, "NOK/y")
    print("\tf75: ", FeAl90.f, "NOK/y")
    print("\tc75: ", FeAl90.o + FeAl90.f, "NOK/y")

problem1()
problem2()
