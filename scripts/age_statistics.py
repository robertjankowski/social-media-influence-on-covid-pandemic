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


def death_rate_ratio(age: int):
    """
    Take into account age when calculating death probability. The 18-29 years old are the comparision group

    Based on `https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html`

    :param age: age of the agent
    """
    if 0 < age < 5:
        return 4
    elif 5 < age < 18:
        return 16
    elif 18 < age < 30:
        return 1
    elif 30 < age < 40:
        return 4
    elif 40 < age < 50:
        return 10
    elif 50 < age < 65:
        return 30
    elif 65 < age < 75:
        return 90
    elif 75 < age < 85:
        return 220
    elif age > 85:
        return 630
