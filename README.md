# GA Knapsack – Diseño Factorial 2³

Código fuente del artículo: "Análisis estadístico del desempeño de un
Algoritmo Genético (GA) para el problema de la mochila 0/1 mediante
diseño factorial 2^k"

## Descripción
Implementación en Python de un algoritmo genético binario aplicado a una
instancia del problema de la mochila 0/1 (n=26, W=80), con un diseño
factorial completo 2³ para evaluar el efecto de la probabilidad de
mutación, probabilidad de cruce y tamaño de población.

## Requisitos
- Python 3.x (solo usa bibliotecas estándar: random, csv, typing)

## Uso
python ga_knapsack.py
Los resultados se guardan en `Aresultados_ga_knapsack.csv`.

## Factores evaluados
| Factor | Nivel bajo (-1) | Nivel alto (+1) |
|--------|----------------|-----------------|
| Probabilidad de mutación | 0.01 | 0.10 |
| Probabilidad de cruce | 0.50 | 0.90 |
| Tamaño de población | 26 | 52 |

## Autores
Villarreal-Romero R., Casillas-Velasco E., Gil-Leal A.,
Galaviz-Mosqueda A. – CICESE Unidad Monterrey

## Licencia
MIT
