from scripts.parameters import *


class SimulationConstants:
    N_AGENTS = 10000
    N_STEPS = 20000
    FRAC_ADDITIONAL_VIRTUAL_LINKS = 0.1
    L1_DEFAULT_PARAMS = PhysicalLayerParameters(0.3, 0.2, 0.9, 0.05)
    L2_VOTER_DEFAULT_PARAMS = QVoterParameters(4, 0.5)
    L2_SOCIAL_MEDIA_DEFAULT_PARAMS = SocialMediaParameters(0.1, 100)

    @staticmethod
    def _get_additional_virtual_links(n):
        return SimulationConstants.FRAC_ADDITIONAL_VIRTUAL_LINKS * n * (n - 1) / 2

    def __init__(self,
                 n_agents=None,
                 n_steps=None,
                 n_additional_virtual_links=None,
                 l1_params=None,
                 l2_voter_params=None,
                 l2_social_media_params=None):
        self.n_agents = n_agents if n_agents is not None else SimulationConstants.N_AGENTS
        self.n_steps = n_steps if n_steps is not None else SimulationConstants.N_STEPS
        self.n_additional_virtual_links = n_additional_virtual_links if n_additional_virtual_links is not None \
            else self._get_additional_virtual_links(self.n_agents)
        self.l1_params = l1_params if l1_params is not None else SimulationConstants.L1_DEFAULT_PARAMS
        self.l2_voter_params = l2_voter_params if l2_voter_params is not None \
            else SimulationConstants.L2_VOTER_DEFAULT_PARAMS
        self.l2_social_media_params = l2_social_media_params if l2_social_media_params is not None \
            else SimulationConstants.L2_SOCIAL_MEDIA_DEFAULT_PARAMS
