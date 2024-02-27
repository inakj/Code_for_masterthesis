""""
Materiale: Y1860S7 (1860 N/mm2, 7 strands)
Diameter 15,2mm med et beregningsmessig areal på 139mm2 (skyldes tomrom mellom wire strands)
Oppspenning: opp til 140 kN pr , også vanligvis en begrensning på benken mellom 4-5000 kN
Kanskje standardverdi kan være 115 kN
"""


eps_po = 
Ep = 1.95 * 10 ** 5
Ap = 139 
fpk = 1860
gamma_s = 1.15
fpd = fpk / gamma_s
Po = eps_po * Ep * Ap # Oppspenningskraft

# If assumed load balanced, then pretension force is given by: (p is distributed external load)
P = (p * L ** 2)/(8 * e)

# Uten / med endeeksentrisitet (på midten)
Mp = P * e2

# assumed e1 = e2 = e:

# Upward deflection becasue of lifting load q and downward deflection becasuse of constant moment for end-ecentricity
deflection = (P * e * L ** 2)/(E * I * 12) 

#Losses

# Strainloss between pretension and concrete

# locking
# friction
# temperature

# Stress change bc of shortterm load

# Time dependant loss


