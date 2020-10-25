from dataclasses import dataclass, field


@dataclass
class VirtualLayerParameters:
    """Parameters of simulation for $$l_1$$ (communication) layer

    p_lambda: probability of agent to become aware of epidemic (U -> A)

    p_delta: probability of agent to forget about epidemic (A -> U)
    """
    p_lambda: float
    p_delta: float


@dataclass
class PhysicalLayerParameters:
    """Parameters of simulation for $$l_2$$ (epidemic) layer

    p_beta: probability that agent becomes infected (S -> I)

    p_gamma: probability that agent goes in a quarantine (I -> Q)

    p_mu: probability that agent recovers from illness (Q -> R)

    p_kappa: (1 - p_mu): probability that agent dies (Q -> D)
    """
    p_beta: float
    p_gamma: float
    p_mu: float

    def __post_init__(self):
        self.p_kappa = 1 - self.p_mu


@dataclass
class QVoterParameters:
    """Parameters of q-voter model in $$l_1$$ (communication) layer

    q: number of neighbours

    p_p: probability that agent acts individually

    p_epsilon: probability that agent change his opinion, when `q` neighbours do not have unanimity opinion.
    """
    q: int
    p_p: float
    p_epsilon: float
