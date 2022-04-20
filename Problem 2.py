# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:54:30 2022

@author: giova
"""

import math
from classes.Objects import Line

P_lo = 1.25     #Off-peak demand [MW]
P_hi_base = 3.5 #Peak demand before chargers [MW]
Pchg = 0.055    #Power per charger [MW]
Nchg = 52
P_hi = P_hi_base + Pchg * Nchg  #[MW]

disc_rate = 0.085 #8.5%

#High and low demand cost and daily duration
Cl = 210 #[NOK/MWh]
Ch = 325 #[NOK/MWh]
Th = 6      #[h]
Tl = 24-Th  #[h]

#Line characteristics:
U=10 #kV
Imax_25 = 0.255 #kA
Length = 8   #[km]
resistivity = 18  #[ohm*mm^2/km]

def problem1():
    print("\nProblem 1:")
    Plim_25 = math.sqrt(3)*U*Imax_25  #MW

    print("Peak power: ",P_hi, " MW")
    print("Base line capacity: ", Plim_25, " MW")

def problem2():
    print("\nProblem 2:")
    P_hi = P_hi_base + Pchg * Nchg
    
    #Option 1: FeAl75 60mm^2 line
    FeAl75 = Line(U,resistivity,Length,60)
    FeAl75.calc_inv_annuity(750000, disc_rate, 20) #
    FeAl75.calc_op_cost(P_lo, P_hi, Ch, Cl, Th)
    
    Wloss_y = (FeAl75.loss(P_lo)*Tl + FeAl75.loss(P_hi)*Th)*365 #Yearly energy loss
    
    print("FeAl75:")
    print("\tYearly loss: ", Wloss_y, " MWh")
    print("\to75: ", FeAl75.o, "NOK/y")
    print("\tf75: ", FeAl75.f, "NOK/y")
    print("\tc75: ", FeAl75.o + FeAl75.f, "NOK/y")
    
    #Option 2: FeAl90 90mm^2 line
    FeAl90 = Line(U,resistivity,Length,90)
    FeAl90.calc_inv_annuity(900000, disc_rate, 20)
    FeAl90.calc_op_cost(P_lo, P_hi, Ch, Cl, Th)
    
    Wloss_y = (FeAl90.loss(P_lo)*Tl + FeAl90.loss(P_hi)*Th)*365 #Yearly energy loss
    
    print("\nFeAl90:")
    print("\tYearly loss: ", Wloss_y, " MWh")
    print("\to90: ", FeAl90.o, "NOK/y")
    print("\tf90: ", FeAl90.f, "NOK/y")
    print("\tc90: ", FeAl90.o + FeAl90.f, "NOK/y")

problem1()
problem2()
