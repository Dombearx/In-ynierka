from subprocess import call

num_of_iterations = ["10000"]

num_of_islands = ["5", "10"]
migration_ratio = ["2", "10", "20"]

models = [
    "convection_const",
    "convection_front",
    "island"
]

benchmarks = [
    "dtlz1",
    "dtlz2",
    "dtlz3",
    "dtlz4"
]
for model in models:
    for benchmarkName in benchmarks:
        for islandNum in num_of_islands:
            for ratio in migration_ratio:
                for maxIterations in num_of_iterations:
                    call(["python", "algorithm_mul.py", benchmarkName, islandNum,
                          ratio, maxIterations, model])
