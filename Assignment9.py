# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:54:30 2022

@author: giova
"""

import math
import classes.EnergySystems as ES

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
    
    #Option 1: FeAl75 60mm^2 line
    FeAl75 = ES.Line(U,resistivity,Length,60)
    FeAl75.calc_fixed_annual(750000, disc_rate, 20) #
    FeAl75.calc_op_cost(P_lo, P_hi, Ch, Cl, Th)
    
    Wloss_y = (FeAl75.loss(P_lo)*Tl + FeAl75.loss(P_hi)*Th)*365 #Yearly energy loss
    
    print("FeAl75:")
    print("\tYearly loss: ", Wloss_y, " MWh")
    print("\to75: ", FeAl75.o, "NOK/y")
    print("\tf75: ", FeAl75.f, "NOK/y")
    print("\tc75: ", FeAl75.o + FeAl75.f, "NOK/y")
    
    #Option 2: FeAl90 90mm^2 line
    FeAl90 = ES.Line(U,resistivity,Length,90)
    FeAl90.calc_fixed_annual(900000, disc_rate, 20)
    FeAl90.calc_op_cost(P_lo, P_hi, Ch, Cl, Th)
    
    Wloss_y = (FeAl90.loss(P_lo)*Tl + FeAl90.loss(P_hi)*Th)*365 #Yearly energy loss
    
    print("\nFeAl90:")
    print("\tYearly loss: ", Wloss_y, " MWh")
    print("\to90: ", FeAl90.o, "NOK/y")
    print("\tf90: ", FeAl90.f, "NOK/y")
    print("\tc90: ", FeAl90.o + FeAl90.f, "NOK/y")
    
def problem4():
    print("\nProblem 4:")
    batt = ES.Battery(0.96, 0.94)
    batt.load_level_cap(P_hi, P_lo, Th)
    
    print("Capacity: ", batt.C, " MWh")
    #Consider line losses and energy lost during charge and discharge of the battery.
    FeAl25 = ES.Line(U,resistivity,Length,25)
    #Power is constant thanks to battery
    ob = (FeAl25.calc_op_cost(batt.Pleveled,batt.Pleveled,Ch,Cl,Th) #line loss
          + batt.calc_leveling_loss_cost(Cl))   #battery loss
    print("ob: ", ob, "NOK/y")
    
    FeAl90 = ES.Line(U,resistivity,Length,90)
    c90 = (FeAl90.calc_fixed_annual(900000, disc_rate, 20) 
           + FeAl90.calc_op_cost(P_lo, P_hi, Ch, Cl, Th))
        
    print("c90: ", c90, "NOK/y")
    print("\nTo ensure positive benefit compared to FeAl90 line, annual fixed cost fb must be less than: \n\tc90-ob =", 
          c90 - ob, 
          " NOK/y")
    F0max = (c90 - ob)/ES.annuity_factor(disc_rate, 20)
    print("Max total fixed cost F0max: ", F0max, " NOK")
    
    # the battery's lifetime is 15 y and the period of analysis is 20y
    # we need to reinvest after 15y, and the new battery will have salvage value 
    # at the end of analysis
    Lbatt=15
    Period=20
    Fmax = (F0max / 
                (1 + 
                (1+disc_rate)**-Lbatt - 
                (2*Lbatt-Period)*((1+disc_rate)**-Period)/Lbatt
            ))
    print("Max initial investment Fmax: ", Fmax, " NOK")

problem1()
problem2()
problem4()
