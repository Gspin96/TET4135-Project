# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:54:30 2022

@author: giova
"""

import math

def res(r, L, A):
        return r*L/A
def annuity(disc, period): 
    return disc/(1-(1+disc)**(-period))

class Line:
    def __init__(self, U, r, L, A ):
        self.U = U
        self.r = r
        self.L = L
        self.A = A
        self.R = r*L/A
    def res(self):
        return self.R;
    
    def loss(self, P):
        return self.R/(self.U**2)*P**2
    def op_cost(self, Pl, Ph, El):
        return 365*(self.loss(Pl)*El.Cl*El.Tl + self.loss(Ph)*El.Ch*El.Th)

Plow = 1.25
Pmax_base = 3.5
Pchg = 0.055
Nchg = 52
disc_rate = 0.085

#High and low demand cost and hours per day
class El:
        Cl = 210
        Ch = 325
        Th = 6
        Tl = 24-Th

#Line characteristics:
U=10 #kV
Imax_25 = 0.255 #kA
L = 8
r = 18 #ohm*mm^2/km     resistivity

Pmax = Pmax_base + Pchg * Nchg    #MW
Plim_25 = math.sqrt(3)*U*Imax_25  #MW

print("Peak power: ",Pmax, " MW")
print("Base line capacity: ", Plim_25, " MW")

#60mm^2 line
FeAl75 = Line(U,r,L,60)
Fkm = 750000
f = Fkm*L*annuity(disc_rate, 20)
Ploss_lo = FeAl75.loss(Plow)    #MW
Ploss_hi = FeAl75.loss(Pmax)     #MW


#Yearly energy loss
Wloss_y = (Ploss_lo*El.Tl + Ploss_hi*El.Th)*365
o = FeAl75.op_cost(Plow,Pmax, El)
print("\nFeAl75 losses:")
print("\tLow demand: ", Ploss_lo, " MW")
print("\tHigh demand: ", Ploss_hi, " MW")
print("\tYearly: ", Wloss_y, " MWh")
print("\to75: ", o, "NOK/y")
print("\tf75: ", f, "NOK/y")
print("\tc75: ", o + f, "NOK/y")

#90mm^2 line
R = res(r,L,90)
Fkm = 900000
f = Fkm*L*annuity(disc_rate, 20)
Ploss_90_low = R/(U**2)*Plow**2     #MW
Ploss_90_max = R/(U**2)*Pmax**2     #MW
"""
#Yearly energy loss
Wloss_y_90 = (Ploss_90_low*dl + Ploss_90_max*dh)*365
Closs_y_90 = (Ploss_90_low*dl*Cl + Ploss_90_max*dh*Ch)*365
print("\nFeAl90 losses:")
print("\tLow demand: ", Ploss_90_low, " MW")
print("\tHigh demand: ", Ploss_90_max, " MW")
print("\tYearly: ", Wloss_y_90, " MWh")
print("\to90: ", Closs_y_90, "NOK/y")
print("\tf90: ", f, "NOK/y")
print("\tc90: ", Closs_y_90 + f, "NOK/y")"""


