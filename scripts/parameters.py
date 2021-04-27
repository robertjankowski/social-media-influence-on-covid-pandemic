from dataclasses import dataclass


@dataclass
class PhysicalLayerParameters:
    """Parameters of simulation for $$l_1$$ (epidemic) layer

    p_beta: probability that agent becomes infected (S -> I)

    p_gamma: probability that agent goes in a quarantine (I -> Q)

    p_mu: probability that agent recovers from illness (Q -> R)

    p_kappa: (1 - p_mu): probability that agent dies (Q -> D)

    p_omega: probability that agent recovers being infected (I -> R)

    p_zeta: probability that agent dies being infected (I -> R)
    """
    p_beta: float
    p_gamma: float
    p_mu: float
    p_omega: float
    p_zeta: float

    def __post_init__(self):
        self.p_kappa = 1 - self.p_mu

    def __str__(self):
        return f'beta={self.p_beta}_gamma={self.p_gamma}_mu={self.p_mu}_kappa={self.p_kappa}_omega={self.p_omega}_zeta={self.p_zeta}'


@dataclass
class QVoterParameters:
    """Parameters of q-voter model in $$l_2$$ (communication) layer

    q: number of neighbours

    p_p: probability that agent acts individually

    """
    q: int
    p_p: float

    def __str__(self):
        return f'q={self.q}_p={self.p_p}'


@dataclass
class SocialMediaParameters:
    """Parameters for social media in $$l_2$$ (communication) layer

    p_xi: probability that agent becomes aware (U -> A)

    n: number of steps when social media is working
    """
    p_xi: float
    n: float

    def __str__(self):
        return f'xi={self.p_xi}_n={self.n}'
