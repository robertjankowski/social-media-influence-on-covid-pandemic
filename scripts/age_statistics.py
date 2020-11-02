import numpy as np


def generate_from_age_gender_distribution(samples: int, gender: str):
    """
    Data collected from: https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/ludnosc-piramida/

    :param gender: Female or Male ('F' or 'M')
    :param samples: Number of agents
    """
    total_population = 0
    probability = []
    ages = []
    with open('../data/poland_population_age_distribution.txt') as f:
        f.readline()  # omit header
        for line in f:
            age, total, males, females = [int(x) for x in line.strip().split('\t')]
            if gender == 'F':
                probability.append(females)
                total_population += females
            elif gender == 'M':
                probability.append(males)
                total_population += males
            ages.append(age)

    return np.random.choice(ages, size=samples, p=np.array(probability) / total_population)
