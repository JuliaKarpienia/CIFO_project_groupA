from base.data import *
from operators.selectors import *
from operators.mutators import *
from operators.crossovers import *
from algorithm.algorithm import GA

# The parameters present in this file are the result of a Grid Search of 15 runs and cross-referencing those results
# with the plots we obtained


# This is the example of a valid dataset from class and it's the format of the data we tested
focus_loss = [[0, 10.2, 16, 4, 6, 12, 7.5, 9],
              [10.2, 0, 4.3, 8, 11, 2.2, 3, 11.5],
              [16, 4.3, 0, 9, 3, 6, 7, 5],
              [4, 8, 9, 0, 11, 10.5, 5, 2],
              [6, 11, 3, 11, 0, 9.8, 4, 10],
              [12, 2.2, 6, 10.5, 9.8, 0, 8, 8],
              [7.5, 3, 7, 5, 4, 8, 0, 10.1],
              [9, 11.5, 5, 2, 10, 8, 10.1, 0]]

# The line where data can be inserted is line 13, on fit_foc_loss = calculate_pop_fit (data)
# The data used at the moment is random -> random_focus_gen()
if __name__ == '__main__':
    fit_foc_loss = calculate_pop_fit(random_focus_gen())

    GA(create_population=create_pop,
       evaluate_population=fit_foc_loss,
       maximization=False,
       gens=200,
       pop_size=50,
       selector=roulette_selection,
       mutator=twors_mutation,
       crossover_operator=improved_cycle_crossover,
       p_c=0.9,
       p_m=0.1,
       elitism=True,
       verbose=True,
       log=True,
       path='log/test_log.csv'
       )
