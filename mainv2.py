import numpy as np
import pandas as pd
import itertools
from openpyxl import Workbook
from ordonnanceur.SchedulerOPSFlow.assets import excel_dir, get_sigma


def compute_times(order, sigma):
    _num_machines = sigma.shape[0]
    _num_tasks = len(order)
    start_times = np.zeros((_num_machines, _num_tasks))
    end_times = np.zeros((_num_machines, _num_tasks))

    for m in range(_num_machines):
        for j, task in enumerate(order):
            if m == 0 and j == 0:
                start = 0
            elif m == 0:
                start = end_times[m][j - 1]
            elif j == 0:
                start = end_times[m - 1][j]
            else:
                start = max(float(end_times[m - 1][j]), float(end_times[m][j - 1]))

            duration = sigma[m][task]
            start_times[m][j] = start
            end_times[m][j] = start + duration

    return start_times, end_times, end_times[-1][-1]

excel_dir()

sigma = np.array(get_sigma())

num_machines, num_tasks = sigma.shape
task_indices = list(range(num_tasks))

results = []
for perm in itertools.permutations(task_indices):
    start, end, makespan = compute_times(perm, sigma)
    if len(results) and makespan < results[-1][-1]:
        results.insert(0, (perm, start, end, makespan))
    else:
        results.append((perm, start, end, makespan))

results = sorted(results, key=lambda x: x[3])
best_order = results[0]
print(best_order)

wb = Workbook()
ws = wb.active
ws.title = "Ordonnancement"

for idx, (perm, start, end, makespan) in enumerate(results):
    ws.append([f"{idx}", f"{makespan}", f"Ordre: {'-'.join([f"J{i}" for i in perm])}"])
    ws.append([""] + list(perm))

    for m in range(num_machines):
        row_start = [f"M{m + 1}"] + list(start[m])
        row_end = [""] + list(end[m])
        ws.append(row_start)
        ws.append(row_end)
    ws.append([])

wb.save("ordonnancement_permutations.xlsx")
