from scripts.parameters import *



class SimulationConstants:
    N_AGENTS = 10000
    N_STEPS = 150000
    L1_DEFAULT_PARAMS = PhysicalLayerParameters(0.1, 0.2, 0.9, 0.05, 10)
    FRACTION_COMORBIDITIES_A = 0.1
    FRACTION_COMORBIDITIES_B = 0.1

    def __init__(self,
                 n_agents=None,
                 n_steps=None,
                 l1_params=None,
                 comorbid_disease_A_fraction=None,
                 comorbid_disease_B_fraction=None):
        self.n_agents = n_agents if n_agents is not None else SimulationConstants.N_AGENTS
        self.n_steps = n_steps if n_steps is not None else SimulationConstants.N_STEPS
        self.l1_params = l1_params if l1_params is not None else SimulationConstants.L1_DEFAULT_PARAMS
        self.comorbid_disease_A_fraction = comorbid_disease_A_fraction if comorbid_disease_A_fraction is not None \
            else SimulationConstants.FRACTION_COMORBIDITIES_A
        self.comorbid_disease_B_fraction = comorbid_disease_B_fraction if comorbid_disease_B_fraction is not None \
            else SimulationConstants.FRACTION_COMORBIDITIES_B
