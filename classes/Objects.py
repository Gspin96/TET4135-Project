# -*- coding: utf-8 -*-

"""
    Line model.
    Initialization parameters:
        U: working voltage
        r: resistivity
        L: length
        A: cross -section
        Name
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
    
    def annuity_factor(self,disc_rate, period): 
        return disc_rate/(1-(1+disc_rate)**(-period))
    
    def calc_inv_annuity(self, Fkm, disc_rate, period):
        self.f = Fkm*self.L*self.annuity_factor(disc_rate, period)
        return self.f
