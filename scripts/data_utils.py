import pandas as pd


def get_value(text):
    return text.split("_")[0]


def load_results(path: str, params):
    all_parameters = {}
    file_name = path.split("/")[-1].split(".csv")[0]
    file_name = file_name.split("=")[1:]

    for i, f in enumerate(file_name):
        all_parameters[params[i]] = get_value(f)

    df = pd.read_csv(path, index_col=0)
    return all_parameters, df


def load_multilayer_results(path: str):
    params = ['beta', 'gamma', 'mu', 'kappa', 'max_infected_time', 'q', 'p', 'xi', 'n', 'n_times', 'n_steps',
              'n_agents', 'n_fraclinks']
    return load_results(path, params)


def load_singlelayer_results(path: str):
    params = ['beta', 'gamma', 'mu', 'kappa', 'max_infected_time', 'FRAC_A', 'FRAC_B', 'n_times', 'n_steps', 'n_agents']
    return load_results(path, params)
