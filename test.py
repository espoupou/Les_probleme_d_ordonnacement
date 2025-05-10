import itertools
import pandas as pd
from openpyxl import Workbook

from ordonnanceur.SchedulerOPSFlow.assets import get_gamma, generate_valid_orders

# Définir les temps de traitement: processing_time[machine][task]
processing_time = [
    [2, 3, 1],  # M1: T1, T2, T3
    [4, 2, 3],  # M2: T1, T2, T3
    [3, 2, 4],  # M3: T1, T2, T3
]

gamma = get_gamma(4)
orders = generate_valid_orders(list(range(4)), gamma)
print(orders)
print(len(orders))
exit()

# Tâches
tasks = ['T1', 'T2', 'T3']
num_machines = len(processing_time)
num_tasks = len(tasks)


# Fonction pour calculer les temps de début/fin pour une permutation
def compute_schedule(order):
    start = [[0] * num_tasks for _ in range(num_machines)]
    end = [[0] * num_tasks for _ in range(num_machines)]

    for j, task_name in enumerate(order):
        task_idx = tasks.index(task_name)
        for m in range(num_machines):
            if m == 0 and j == 0:
                start[m][j] = 0
            elif m == 0:
                start[m][j] = end[m][j - 1]
            elif j == 0:
                start[m][j] = end[m - 1][j]
            else:
                start[m][j] = max(end[m - 1][j], end[m][j - 1])
            end[m][j] = start[m][j] + processing_time[m][task_idx]
    makespan = end[-1][-1]
    return start, end, makespan


# Générer toutes les permutations et les classer par makespan
permutations = list(itertools.permutations(tasks))
results = []
for perm in permutations:
    start, end, makespan = compute_schedule(perm)
    results.append((perm, start, end, makespan))

# Trier les permutations par makespan
results.sort(key=lambda x: x[3])

# Création d'un fichier Excel
wb = Workbook()
ws = wb.active
ws.title = "Ordonnancement"

# Insérer les résultats dans le fichier Excel
for idx, (perm, start, end, makespan) in enumerate(results):
    ws.append([f"Ordre: {'-'.join(perm)}", f"Makespan: {makespan}"])
    ws.append([""] + list(perm))

    for m in range(num_machines):
        row_start = [f"M{m + 1}"] + start[m]
        row_end = [""] + end[m]
        ws.append(row_start)
        ws.append(row_end)

    ws.append([])  # Ligne vide pour séparer

# Sauvegarde (à adapter selon ton environnement)
wb.save("ordonnancement_permutations.xlsx")
