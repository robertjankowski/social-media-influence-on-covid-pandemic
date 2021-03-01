import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    N = [100, 1000, 10000]
    t1 = np.array([977.13, 7633.74, 73122.74])  # N_STEPS = 10000
    t2 = np.array([1865.90, 15072.08, 144255.00])  # N_STEPS = 20000
    t1 /= 12  # number of realizations / parameters
    t2 /= 12
    t1 /= 60  # in minutes
    t2 /= 60

    plt.grid(alpha=0.1)
    plt.plot(N, t1, 'o-', label='N_STEPS=10000', linewidth=3, color='red')
    plt.plot(N, t2, 'o-', label='N_STEPS=20000', linewidth=3, color='blue')
    plt.ylabel('Time [min]')
    plt.xlabel('Network size')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    # plt.savefig('measure_time_simulation_results.pdf', bbox_inches='tight')
    plt.show()
