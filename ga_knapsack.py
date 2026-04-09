import random
import csv
from typing import List

# ==========================================
#  Definiciones del Problema
# ==========================================

class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


class Individual:
    def __init__(self, bits: List[int]):
        self.bits = bits
    
    def __str__(self):
        return repr(self.bits)

    def __hash__(self):
        return hash(str(self.bits))
    
    def fitness(self) -> float:
        total_value = sum(bit * item.value for item, bit in zip(items, self.bits))
        total_weight = sum(bit * item.weight for item, bit in zip(items, self.bits))

        if total_weight <= MAX_KNAPSACK_WEIGHT:
            return total_value
        
        return 0


MAX_KNAPSACK_WEIGHT = 80
REPRODUCTION_RATE = 0.15
NUM_GENERATIONS = 500


items = [
    Item("A", 5, 15), Item("B", 1, 3), Item("C", 8, 45), Item("D", 2, 30),
    Item("E", 17, 60), Item("F", 1, 5), Item("G", 10, 50), Item("H", 9, 20),
    Item("I", 4, 35), Item("J", 3, 18), Item("K", 6, 10), Item("L", 15, 65),
    Item("M", 7, 22), Item("N", 4, 8), Item("O", 3, 40), Item("P", 1, 1),
    Item("Q", 18, 70), Item("R", 10, 28), Item("S", 13, 33), Item("T", 22, 85),
    Item("U", 14, 38), Item("V", 16, 42), Item("W", 3, 12), Item("X", 19, 55),
    Item("Y", 2, 9), Item("Z", 8, 17)
]


# ==========================================
#  GA: Funciones Base
# ==========================================

def generate_initial_population(count: int) -> List[Individual]:
    """Genera población inicial variada sin duplicados."""
    population = set()
    while len(population) < count:
        bits = [random.choice([0, 1]) for _ in items]
        population.add(Individual(bits))
    return list(population)


def selection(population: List[Individual]) -> List[Individual]:
    """Torneo de 3 individuos: mejora estabilidad."""
    def tournament():
        contenders = random.sample(population, 3)
        return max(contenders, key=lambda ind: ind.fitness())
    return [tournament(), tournament()]


def crossover(parents: List[Individual]) -> List[Individual]:
    """Cruce de un punto aleatorio."""
    N = len(items)
    point = random.randint(1, N - 1)

    p1, p2 = parents[0].bits, parents[1].bits

    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]

    return [Individual(child1), Individual(child2)]


def mutate(child: Individual, mutation_rate: float):
    """Mutación bit a bit."""
    child.bits = [
        1 - bit if random.random() < mutation_rate else bit
        for bit in child.bits
    ]


def next_generation(population: List[Individual], crossover_rate: float, mutation_rate: float) -> List[Individual]:
    next_gen = []

    while len(next_gen) < len(population):

        parents = selection(population)

        # Reproducción directa
        if random.random() < REPRODUCTION_RATE:
            children = [Individual(parents[0].bits[:]), Individual(parents[1].bits[:])]
        else:
            # Cruce
            if random.random() < crossover_rate:
                children = crossover(parents)
            else:
                # Sin cruce → copiar padres
                children = [Individual(parents[0].bits[:]), Individual(parents[1].bits[:])]

        # Mutación SIEMPRE aplicada bit-a-bit
        for child in children:
            mutate(child, mutation_rate)

        next_gen.extend(children)

    return next_gen[:len(population)]


# ==========================================
#  GA Principal
# ==========================================

def solve_knapsack(pob_size: int, p_cruz: float, p_mut: float) -> float:
    population = generate_initial_population(pob_size)

    for _ in range(NUM_GENERATIONS):
        population = next_generation(population, p_cruz, p_mut)

    best = max(population, key=lambda ind: ind.fitness())
    return best.fitness()


# ==========================================
#  Diseño Factorial 2^3
# ==========================================

def run_factorial_experiment(num_replicas: int):

    LEVELS = {
        'P_mut': {'low': [0.01], 'high': [0.1]},
        'P_cruz': {'low': [0.5], 'high': [0.9]},
        'PobSize': {'low': [26], 'high': [52]}
    }

    combinations = [
        (LEVELS['P_mut']['low'][0], LEVELS['P_cruz']['low'][0], LEVELS['PobSize']['low'][0], '(1)'),
        (LEVELS['P_mut']['high'][0], LEVELS['P_cruz']['low'][0], LEVELS['PobSize']['low'][0], 'a'),
        (LEVELS['P_mut']['low'][0], LEVELS['P_cruz']['high'][0], LEVELS['PobSize']['low'][0], 'b'),
        (LEVELS['P_mut']['high'][0], LEVELS['P_cruz']['high'][0], LEVELS['PobSize']['low'][0], 'ab'),
        (LEVELS['P_mut']['low'][0], LEVELS['P_cruz']['low'][0], LEVELS['PobSize']['high'][0], 'c'),
        (LEVELS['P_mut']['high'][0], LEVELS['P_cruz']['low'][0], LEVELS['PobSize']['high'][0], 'ac'),
        (LEVELS['P_mut']['low'][0], LEVELS['P_cruz']['high'][0], LEVELS['PobSize']['high'][0], 'bc'),
        (LEVELS['P_mut']['high'][0], LEVELS['P_cruz']['high'][0], LEVELS['PobSize']['high'][0], 'abc'),
    ]

    fieldnames = ['P_mut', 'P_cruz', 'PobSize', 'Combination', 'Replica', 'Best_Fitness']

    with open('Aresultados_ga_knapsack.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for p_mut, p_cruz, pob_size, label in combinations:
            print(f"Running combination {label}: P_mut={p_mut}, P_cruz={p_cruz}, PobSize={pob_size}")

            for r in range(1, num_replicas + 1):

                best_fitness = solve_knapsack(pob_size, p_cruz, p_mut)

                writer.writerow({
                    'P_mut': p_mut,
                    'P_cruz': p_cruz,
                    'PobSize': pob_size,
                    'Combination': label,
                    'Replica': r,
                    'Best_Fitness': best_fitness
                })

                print(f"  Replica {r}: Fitness = {best_fitness}")

    print("\nExperimentación completada. Resultados guardados en 'Aresultados_ga_knapsack.csv'")


if __name__ == '__main__':
    run_factorial_experiment(num_replicas=50)
