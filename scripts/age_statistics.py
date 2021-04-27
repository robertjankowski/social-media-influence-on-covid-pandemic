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
    Take into account age when calculating death probability. The 18-29 years old are the comparison group

    Based on `https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html`

    :param age: age of the agent
    """
    total = 13827
    if 0 <= age < 5:
        return 1 / total
    elif 5 <= age < 18:
        return 1 / total
    elif 18 <= age < 30:
        return 10 / total
    elif 30 <= age < 40:
        return 45 / total
    elif 40 <= age < 50:
        return 130 / total
    elif 50 <= age < 65:
        return 440 / total
    elif 65 <= age < 75:
        return 1300 / total
    elif 75 <= age < 85:
        return 3200 / total
    elif age >= 85:
        return 8700 / total
