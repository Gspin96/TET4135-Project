# -*- coding: utf-8 -*-


def annuity_factor(disc_rate, period): 
        return disc_rate/(1-(1+disc_rate)**(-period))
    

"""----------------------------------------------------------------------------
    Line model.
    Initialization parameters:
        U: working voltage
        r: resistivity
        L: length
        A: cross -section
        Name: For printing information [TODO]
"""
class Line:
    def __init__(self, U, resistivity, length, A, Name="Line" ):
        self.U = U
        self.r = resistivity
        self.L = length
        self.A = A
        self.R = resistivity*length/A
        self.Name = Name
    
    #power loss from line at a given load P
    def loss(self, P):
        return self.R/(self.U**2)*P**2 
    
    #Yearly cost of operation for two daily load levels
    #   Pl: low demand power
    #   Ph: high demand power
    #   Ch: peak electricity cost
    #   Cl: low electricity cost
    #   Th: daily peak duration [h]
    def calc_op_cost(self, Pl, Ph, Ch, Cl, Th):
        self.o = 365*(self.loss(Pl)*Cl*(24-Th) + self.loss(Ph)*Ch*Th)
        return self.o
    
    # Calculate fixed annual cost, assuming lifetime matches period of analysis
    def calc_fixed_annual(self, Fkm, disc_rate, period):
        self.f = Fkm*self.L*annuity_factor(disc_rate, period)
        return self.f
    
    # Set new value for the section and recalculate resistance 
    def set_section(self, A):
        self.A = A
        self.R = self.r*self.L/A


"""----------------------------------------------------------------------------
    Battery model.
    Initialization parameters:
        Chg_eff: charging efficiency 
        Disch_eff: discharging efficiency
        Name: For printing information [TODO]

"""
class Battery:
    def __init__(self, Chg_eff, Disch_eff, Name="Battery" ):
        self.Chg_eff = Chg_eff
        self.Disch_eff = Disch_eff
        self.Name = Name
    
    # Given two daily demand levels and periods, calculate and return battery 
    # capacity needed to flatten load curve.
    # Also calculates daily charge/discharge losses and leveled power import 
    # to store as attributes of the Battery.
    #   Ph: high demand power
    #   Pl: low demand power
    #   Th: daily peak duration [h]
    def load_level_cap(self, Ph, Pl, Th):
        Tl = 24 - Th
        Pdisch = (Ph-Pl)/(Th/Tl/self.Chg_eff/self.Disch_eff + 1)
        self.C=Pdisch*Th/self.Chg_eff
        self.Pleveled = Ph-Pdisch
        self.Disch_loss = Th * Pdisch * (1/self.Disch_eff - 1)
        self.Chg_loss = Tl * (self.Pleveled - Pl) * (1 - self.Chg_eff)
        return self.C
    
    # While operating to flatten load, the battery experiences losses.
    # Calculate the cost of these losses, given the cost of electricity 
    # used for charging. 
    # Requires that load_level_cap(Ph, Pl, Th) has been executed on this Battery
    # to compute losses
    def calc_leveling_loss_cost(self, Cl):
        self.Leveling_loss_cost = (self.Disch_loss+self.Chg_loss)*365*Cl
        return self.Leveling_loss_cost
