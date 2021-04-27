from dataclasses import dataclass


@dataclass
class PhysicalLayerParameters:
    """Parameters of simulation for $$l_1$$ (epidemic) layer

    p_beta: probability that agent becomes infected (S -> I)

    p_gamma: probability that agent goes in a quarantine (I -> Q)

    p_mu: probability that agent recovers from an illness (Q -> R)

    p_kappa: probability that agent dies (Q -> D)
    """
    p_beta: float
    p_gamma: float
    p_mu: float
    p_kappa: float

    def __str__(self):
        return f'beta={self.p_beta}_gamma={self.p_gamma}_mu={self.p_mu}_kappa={self.p_kappa}'


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
