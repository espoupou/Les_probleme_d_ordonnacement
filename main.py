import numpy as np
import itertools

from ordonnanceur.SchedulerOPSFlow.assets import get_sigma


def compute_makespan_with_endtime(order, sigma):
    num_machines = sigma.shape[0]
    end_times = np.zeros((num_machines, len(order)))

    for m in range(num_machines):
        for j, task in enumerate(order):
            if m == 0 and j == 0:
                end_times[m][j] = sigma[m][task]
            elif m == 0:
                end_times[m][j] = end_times[m][j-1] + sigma[m][task]
            elif j == 0:
                end_times[m][j] = end_times[m-1][j] + sigma[m][task]
            else:
                end_times[m][j] = max(int(end_times[m-1][j]), int(end_times[m][j-1])) + sigma[m][task]

    return end_times



sigma = np.array(get_sigma())

num_machines, num_tasks = sigma.shape
task_indices = list(range(num_tasks))

# Test sur toutes les permutations
results = []
for perm in itertools.permutations(task_indices):
    makespan = compute_makespan_with_endtime(perm, sigma)
    results.append((perm, makespan))

# Afficher les 5 meilleures
top5 = sorted(results, key=lambda x: x[1])[:5]
for i, (order, ms) in enumerate(top5, 1):
    print(f"{i}. Ordre: {order}, Makespan: {ms}")
