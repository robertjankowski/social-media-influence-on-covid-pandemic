from scripts.parameters import *


@dataclass
class SimulationConstants:
    N_AGENTS = 1000
    N_STEPS = 20000
    N_ADDITIONAL_VIRTUAL_LINKS = 1000
    INIT_INFECTED_FRACTION = 0.01
    INIT_AWARE_FRACTION = 0.01
    L1_DEFAULT_PARAMS = PhysicalLayerParameters(0.3, 0.2, 0.95)
    L2_DEFAULT_PARAMS = VirtualLayerParameters(0.4, 0.1)
    L2_VOTER_DEFAULT_PARAMS = QVoterParameters(4, 0.5, 0.3)
    L2_SOCIAL_MEDIA_DEFAULT_PARAMS = SocialMediaParameters(0.1, 100)
