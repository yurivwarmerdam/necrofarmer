def lumped_capacity_dt_dt(T, I, R20, Rth, C, T_amb):
    """
    Calculates the rate of temperature change (dT/dt) for a lumped capacity model.
    
    Parameters:
    T     : float - Current temperature of the component (C or K)
    t     : float - Current time (s) [required for ODE solvers, even if unused]
    I     : float - Electrical current (A)
    R20   : float - Electrical resistance at 20°C (Ohms)
    Rth   : float - Thermal resistance (K/W or C/W)
    C     : float - Thermal capacitance (J/K or J/C)
    T_amb : float - Ambient temperature (C or K)
    
    Returns:
    float - dT/dt, the rate of temperature change (K/s or C/s)
    """
    joule_heating = (I ** 2) * R20
    heat_loss = (T - T_amb) / Rth
    
    dT_dt = (joule_heating - heat_loss) / C
    return dT_dt

iteraitons=240
I=19.118
R20=0.025 #tbd variable
Rth=5.7
C=25
T_amb=20 #tbd variable


def iterate_cap(iterations):
    idx=0
    current_tmp=T_amb

    while idx<iterations:
        dT=lumped_capacity_dt_dt(T=current_tmp,I=I,R20=R20,Rth=Rth,C=C,T_amb=T_amb)
        current_tmp+=dT
        print(dT,current_tmp,T_amb)
        idx+=1


iterate_cap(240)