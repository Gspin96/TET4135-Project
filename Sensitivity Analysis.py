""" Sensitivity Analysis.py """
import numpy as np
import matplotlib.pyplot as plt
import classes.EnergySystems as ES

P_lo = 1.25     #Off-peak demand [MW]
P_hi_base = 3.5 #Peak demand before chargers [MW]
Pchg = 0.055    #Power per charger [MW]
Nchg = 52
P_hi = P_hi_base + Pchg * Nchg  #[MW]

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
    
def break_even(Lbatt, disc_rate, Chg_eff, Disc_eff, Ch, Cl):
    s = disc_rate/100
    batt = ES.Battery(Chg_eff, Disc_eff)
    batt.load_level_cap(P_hi, P_lo, Th)
    #Consider line losses and energy lost during charge and discharge of the battery.
    FeAl25 = ES.Line(U,resistivity,Length,25)
    #Power is constant thanks to battery
    ob = (FeAl25.calc_op_cost(batt.Pleveled,batt.Pleveled,Ch,Cl,Th) #line loss
          + batt.calc_leveling_loss_cost(Cl))   #battery loss
    
    FeAl90 = ES.Line(U,resistivity,Length,90)
    c90 = (FeAl90.calc_fixed_annual(900000, s, 20) 
           + FeAl90.calc_op_cost(P_lo, P_hi, Ch, Cl, Th))
    F0max = (c90 - ob)/ES.annuity_factor(s, 20)
    
    # the battery's lifetime is 15 y and the period of analysis is 20y
    # we need to reinvest after 15y, and the new battery will have salvage value 
    # at the end of analysis
    Period=20
    Fmax = (F0max / 
                (1 + 
                (1+s)**-Lbatt - 
                (2*Lbatt-Period)*((1+s)**-Period)/Lbatt
            ))
    return Fmax/1e6 #result in MNOK
    
def lifetime_sensitivity():
    #Calculate Fmax while varying lifetime from 10 to 20 years
    Fmax = {}
    for Lbatt in range(10,21):
        Fmax[Lbatt] = break_even(Lbatt, 8.5, 0.96, 0.94, Ch, Cl)
    print("Fmax[Lbatt]: ", Fmax, " [MNOK]")
    
    x, y = zip(*sorted(Fmax.items()))
    
    plt.plot(x, y, "sr")
    plt.plot(x, y)
    plt.xticks(range(10,21))
    plt.grid()
    plt.xlabel('Battery lifetime [y]')
    plt.ylabel('Break-even cost [MNOK]')
    plt.title('Sensitivity analysis of break-even cost\n(Lifetime)')
    plt.show()
   
def discount_sensitivity():
    #Calculate Fmax while varying discount rate from 2% to 10%
    Fmax = {}
    for disc_rate in range(2,11):
        Fmax[disc_rate] = break_even(15, disc_rate, 0.96, 0.94, Ch, Cl)
    print("Fmax[Lbatt]: ", Fmax, " [MNOK]")
    
    x, y = zip(*sorted(Fmax.items()))
    
    plt.plot(x, y, "sr")
    plt.plot(x, y)
    plt.yticks(np.arange(-1,3,0.5))
    plt.grid()
    plt.xlabel('Discount rate [%]')
    plt.ylabel('Break-even cost [MNOK]')
    plt.title('Sensitivity analysis of break-even cost\n(Discount rate)')
    plt.show()
     
def efficiency_sensitivity():
    #Calculate Fmax while varying efficiency from 90 to 100%
    Fmax = {}
    for eff in range(90,100):
        Fmax[eff] = break_even(15, 8.5, eff/100, eff/100, Ch, Cl)
    print("Fmax[Lbatt]: ", Fmax, " [MNOK]")
    
    x, y = zip(*sorted(Fmax.items()))
    
    plt.plot(x, y, "sr")
    plt.plot(x, y)
    plt.grid()
    plt.xlabel('Efficiency [%]')
    plt.ylabel('Break-even cost [MNOK]')
    plt.title('Sensitivity analysis of break-even cost\n(Efficiency)')
    plt.show()
    
def peak_cost_sensitivity():
    #Calculate Fmax while varying high demand electricity cost from 260 to 400 NOK/MWh 
    Fmax = {}
    for C_peak in range(260,400,20):
        Fmax[C_peak] = break_even(15, 8.5, 0.96, 0.94, C_peak, Cl)
    print("Fmax[Lbatt]: ", Fmax, " [MNOK]")
    
    x, y = zip(*sorted(Fmax.items()))
    
    plt.plot(x, y, "sr")
    plt.plot(x, y)
    plt.grid()
    plt.xlabel('Peak energy cost [NOK/MWh]')
    plt.ylabel('Break-even cost [MNOK]')
    plt.title('Sensitivity analysis of break-even cost\n(Peak energy cost)')
    plt.show()


lifetime_sensitivity()
discount_sensitivity()
efficiency_sensitivity()
peak_cost_sensitivity()
