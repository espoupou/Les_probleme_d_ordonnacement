from collections import defaultdict
from os import getcwd, mkdir

class NotBinaryValueError(Exception):
    def __init__(self, invalid_value):
        super().__init__(f"Valeur invalide trouvée: {invalid_value}. Seul 0 ou 1 sont autorisées.")
        self.invalid_value = invalid_value

class CircularConstraintError(Exception):
    def __init__(self, iv0, iv1):
        super().__init__(f"Contrainte Invalide : J{iv1} depend déjà de J{iv0}.")

def get_sigma():
    a, line = [], []
    print("Entrer les coefficients σ[x, y] des durées séparées par des espaces")

    while True:
        try:
            n = int(input("nombre de machine : "))
            assert n > 0
            break
        except ValueError:
            print("La valeur n'est pas correcte.")
        except AssertionError:
            print("Le nombre de machine doit être positif.")

    j = 0
    for i in range(n):
        print(f"M{i} : ", end='')
        while True:
            try:
                line = list(map(float, input().split(' ')))
                if i == 0:
                    j = len(line) - 1
                assert len(line) == j + 1
                a.append(line)
                break
            except ValueError:
                print("Les valeurs ne sont pas corrects")
            except AssertionError:
                print(f"le nombre de Job entré sur la machine ({len(line)}) est different du nombre defini ({n + 1})")
            print("ressaisissez la ligne : ", end='')
        i += 1
    return a


def get_gamma(n:int = 0):
    a, line = [], []
    print("Entrer les γ[x] dependants de  Ty séparées par des espaces (0 pour non ou 1 pour oui) : ")

    j = 0
    for i in range(n):
        print(f"J{i} : ", end='')
        while True:
            try:
                line = list(map(float, input().split(' ')))
                assert len(line) == n

                for index, value in enumerate(line):
                    if value not in (0, 1):
                        raise NotBinaryValueError(value)
                    if value == 1:
                        if (i, index) in a or i == index:
                            raise CircularConstraintError(i, index)
                        a.append((index, i))
                break
            except ValueError:
                print("Les valeurs ne sont pas corrects")
            except NotBinaryValueError:
                print("Les seules valeurs autorisées sont 0 ou 1")
            except CircularConstraintError as e:
                print("Erreur de dependence mutuelle: ", e)
            except AssertionError:
                print(f"le nombre de contraintes entrées sur le J{i} est different du nombre Total de Job ({n})")
            print("ressaisissez la ligne : ", end='')
    return a


def generate_valid_orders(tasks, constraints):
    graph = defaultdict(list)
    in_degree = {task: 0 for task in tasks}

    for before, after in constraints:
        graph[before].append(after)
        in_degree[after] += 1

    results = []

    def backtrack(current_order, available_tasks, in_degree_copy):
        if len(current_order) == len(tasks):
            results.append(current_order[:])
            return

        for task in sorted(available_tasks):  # Optionnel : trie pour cohérence
            next_available = available_tasks - {task}
            updated_in_degree = in_degree_copy.copy()

            for neighbor in graph[task]:
                updated_in_degree[neighbor] -= 1
                if updated_in_degree[neighbor] == 0:
                    next_available.add(neighbor)

            backtrack(current_order + [task], next_available, updated_in_degree)

    starters = {task for task in tasks if in_degree[task] == 0}
    backtrack([], starters, in_degree)

    return results


def excel_dir():
    try:
        mkdir(f"{getcwd()}/order")
    except FileExistsError:
        pass