from scripts.parameters import *


class SimulationConstants:
    N_AGENTS = 1000
    N_STEPS = 20000
    N_ADDITIONAL_VIRTUAL_LINKS = 1000
    INIT_INFECTED_FRACTION = 0.01
    INIT_AWARE_FRACTION = 0.01
    L1_DEFAULT_PARAMS = PhysicalLayerParameters(0.3, 0.2, 0.9, 0.5, 0.3)
    L2_DEFAULT_PARAMS = VirtualLayerParameters(0.4, 0.1)
    L2_VOTER_DEFAULT_PARAMS = QVoterParameters(4, 0.5)
    L2_SOCIAL_MEDIA_DEFAULT_PARAMS = SocialMediaParameters(0.1, 100)

    def __init__(self,
                 n_agents=None,
                 n_steps=None,
                 n_additional_virtual_links=None,
                 init_infection_fraction=None,
                 init_aware_fraction=None,
                 l1_params=None,
                 l2_params=None,
                 l2_voter_params=None,
                 l2_social_media_params=None):
        self.n_agents = n_agents if n_agents is not None else SimulationConstants.N_AGENTS
        self.n_steps = n_steps if n_steps is not None else SimulationConstants.N_STEPS
        self.n_additional_virtual_links = n_additional_virtual_links if n_additional_virtual_links is not None \
            else SimulationConstants.N_ADDITIONAL_VIRTUAL_LINKS
        self.init_infection_fraction = init_infection_fraction if init_infection_fraction is not None \
            else SimulationConstants.INIT_INFECTED_FRACTION
        self.init_aware_fraction = init_aware_fraction if init_aware_fraction is not None \
            else SimulationConstants.INIT_AWARE_FRACTION
        self.l1_params = l1_params if l1_params is not None else SimulationConstants.L1_DEFAULT_PARAMS
        self.l2_params = l2_params if l2_params is not None else SimulationConstants.L2_DEFAULT_PARAMS
        self.l2_voter_params = l2_voter_params if l2_voter_params is not None \
            else SimulationConstants.L2_VOTER_DEFAULT_PARAMS
        self.l2_social_media_params = l2_social_media_params if l2_social_media_params is not None \
            else SimulationConstants.L2_SOCIAL_MEDIA_DEFAULT_PARAMS
