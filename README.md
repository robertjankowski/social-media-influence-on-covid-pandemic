# social-media-influence-on-covid-pandemic
Simulation of the COVID pandemic on the bilayer network and study the influence of social media on behaviors of individuals. 

![](plots/initial_network_state.png)
The project aims to scrutinize the influence of social media on the global pandemic, COVID-19. It leverages methods from complex networks to describe how awareness of the agents enlists the total dead ratio and infected ratio. The simulations were performed on the duplex network:

- (1a) virtual contacts layer
- (1b) social media layer
- (2) physical contacts layer

**Ad (1a)**  In the virtual contacts layer each agent can be in two states: A (aware), U (unaware). If an agent is in the A state, he knows about the epidemic. This layer has two parameters:
- \lambda -- the probability that the agent will be acknowledged about the epidemic.
- \delta -- the probability that the agent will forget about the epidemic.

![](plots/presentation/sieci_wielopoziomowe_komunikacjadrawio.png)

Moreover, the agent has an opinion about the epidemic safety rules (+1 or -1). For instance, opinion +1 means a positive attitude towards e.g. quarantine and vaccination. As the result, the rules of the q-voter model are also simulating. The figure below depicts the update algorithm for the randomly selected agent.

![q-voter-schema](plots/presentation/q-voter-schema.png)

**Ad (1b)** Every `n` steps all agents can become aware of the epidemic with the probability \xi due to the social media.


**Ad (2).** In the physical contacts layer, each agent can be in 5 states: S (susceptible), I (infected), Q (quarantined), R (recovered),  D (dead). 
Parameters:
- \beta -- infection probability
- \gamma -- the probability of going into quarantine
- \mu -- recovery probability 
- \kappa -- death probability


![](plots/presentation/sieci_wielopoziomowe_epidemia_schemat.png)

### Simulation parameters:

- number of agents N = 100
- number of additional links in the virtual contact layer E = 200
- number of simulation steps N_STEPS = 20000
- the percent of infected agents: 5%
- the percent of aware agents: 5%
- the person coefficient between layers: r ~= 0.97

## Experiments

### Experiment A

**How the size of the lobby in the q-voter model and the probability of independence alter the toll of deaths?**


### Experiment B

**To what extend the social media makes an impact on the infected and dead ratio?**
