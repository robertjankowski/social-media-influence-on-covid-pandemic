from scripts.simulation import init_run_simulation
from scripts.parameters import *
from scripts.epidemic_metrics import *
from scripts.virtual_metrics import *

DEFAULT_L1_PARAMS = PhysicalLayerParameters(0.2, 0.6, 0.999)
DEFAULT_L2_PARAMS = VirtualLayerParameters(0.4, 0.6)
DEFAULT_L2_VOTER_PARAMS = QVoterParameters(3, 0.1, 0.3)
DEFAULT_L2_SOCIAL_MEDIA_PARAMS = SocialMediaParameters(0.1, 1)

metrics = {'aware_ratio': ('l2_layer', aware_ratio),
           'unaware_ratio': ('l2_layer', unaware_ratio),
           'infected_ratio': ('l1_layer', infected_ratio),
           'dead_ratio': ('l1_layer', dead_ratio),
           'quarantined_ratio': ('l1_layer', quarantined_ratio),
           'recovered_ratio': ('l1_layer', recovered_ratio),
           'susceptible_ratio': ('l1_layer', susceptible_ratio),
           'mean_opinion': ('l2_layer', mean_opinion)}

N_AGENTS = 500
N_STEPS = 10000
N_ADDITIONAL_VIRTUAL_LINKS = 2000
INIT_INFECTED_FRACTION = 0.01
INIT_AWARE_FRACTION = 0.01


def perform_simulation(l1_params=DEFAULT_L1_PARAMS,
                       l2_params=DEFAULT_L2_PARAMS,
                       l2_voter_params=DEFAULT_L2_VOTER_PARAMS,
                       l2_social_media_params=DEFAULT_L2_SOCIAL_MEDIA_PARAMS):
    return init_run_simulation(
        N_AGENTS,
        N_ADDITIONAL_VIRTUAL_LINKS,
        INIT_INFECTED_FRACTION,
        INIT_AWARE_FRACTION,
        N_STEPS,
        l1_params,
        l2_params,
        l2_voter_params,
        l2_social_media_params,
        metrics,
        verbose=True)
