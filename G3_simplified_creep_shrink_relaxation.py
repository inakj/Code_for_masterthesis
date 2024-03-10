
class time_dependant_losses:

    def __init__(self,material,cross_section,t,creep,sigma_c_prestress,eps_cs):
        self.delta_relaxation = self.calc_delta_sigma_pr(material.fpk,material.fp01,cross_section.e,t)
        self.delta_sigma_reduction = self.calc_stress_reduction(eps_cs,material.Ep,material.Ecm,self.delta_relaxation,creep.phi,sigma_c_prestress,cross_section.Ap,cross_section.Ac,cross_section.Ic,cross_section.e) 

# Loss because of relaxation
    def calc_delta_sigma_pr(self,fpk: float,fp01k: float,e: float ,t = 500000) -> float:
        """
        Calculation of loss in stress because of relaxation, where the steel is exposed to constant strain for long time. EC2 3.3.2.(7). Assumed class 2: low relaxation
        Args:
            sigma_pi is the absolute value of the intial prestress
            ro_1000 is a percentage of the initial tension sigma_pi EC", 3.3.2(6)
            t is time after stress-application, assumed t = 500 000 (ca 57 years)
            fpk is characteristic strength for prestress
            fp01k is 0.1% limit of strength for prestress
        Returns:
            Absolute value of relaxation lodd i N/mm2
        """
        sigma_pi = abs(min(0.75 * fpk, 0.85 * fp01k))
        ro_1000 = 2.5
        my = sigma_pi / fpk
        delta_sigma_pr = sigma_pi * (0.66 * ro_1000 * e ** (9.1 * my) * (t / 1000) ** (0.75 * (1 - my)) * 10 ** (-5))
        return delta_sigma_pr

# Total time dependant stress reduction in prestress, simplfied: 
    def calc_stress_reduction(self,eps_cs: float,Ep: float,Ecm: float,delta_sigma_pr: float,phi: float,sigma_c_QP: float,Ap: float,Ac: float,Ic: float,zcp: float) -> float:
        """
        Total time dependant stress reduction in prestress, simplfied from EC2 5.10.6(2)
        Args:
            eps_cs is free shrink strain (absolute value) (In F2_Deflection_longterm)
            Ep is elasticity modulus for prestress
            Ecm is elasticity modulus for concrete
            delta_sigma_pr is stressloss because of relaxation (absolute value)
            phi is creep number, phi(t,t0), where t = 50 years and t0 is days after self load application(F4_phi)
            sigma_c_QP is concrete stress in line with prestress for permanent load (absolute value) (G1)
            Ap is cross-section area of prestress
            Ac is cross-section area of concrete
            Ic is moment of inertia for concrete cross_section
            zcp is eccentricity of prestress = e
        Return:
            Reduction in N/mm2
        """
        delta_sigma_p = (eps_cs * Ep + 0.8 * delta_sigma_pr + (Ep / Ecm) * phi * sigma_c_QP) / (1 + (Ep / Ecm) * (Ap / Ac) * (1 + (Ac / Ic) * zcp ** 2) * (1 + 0.8 * phi))
        return delta_sigma_p
    
