from algorithm.parameters import params
from fitness.evaluation import evaluate_fitness
from stats.stats import stats, get_stats
from utilities.stats import trackers


def search_loop():
    """
    This is a standard search process for an evolutionary algorithm. Loop over
    a given number of generations.
    
    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """

    print(params['INITIALISATION'], params['POPULATION_SIZE']) # Added by me as a debug - REMOVE
    # Initialise population
    individuals = params['INITIALISATION'](params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness(individuals)

    # Generate statistics for run so far
    get_stats(individuals)

    # Traditional GE
    for generation in range(1, (params['GENERATIONS']+1)):
        stats['gen'] = generation

        # New generation
        individuals = params['STEP'](individuals)


    #ROISIN: To save phenotype of best individual
    run_no = int(params["EXTRA_PARAMETERS"])
    print("RUN_NO: ", run_no)

    best=max(individuals)
    print("Best: ", best)
    ind=best.phenotype
    length = len(ind)
    i = 0
    # Wrie best to file and play with midi
    instruments = ["kick", "hh", "hhOp", "snH", "Sin1", "Sin2"]
    bestfile = open("../results/ChucK/" + instruments[run_no] + ".ck", 'w')
    """ Separate individaul into lines and add to file"""
    while i < length:
        # print i
        try:
            end_line = ind.index(";")
            # print "ind: %s end: %d, i: %d"%(ind, end_line, i)
            line = ind[: end_line + 1]

            try:
                if line[0] == "L":
                    bestfile.write("while (true) \n { \n")
                    line = line[1:]

            except IndexError:
                pass
            bestfile.write(str(line))
            bestfile.write("\n")
            ind = ind[end_line + 1:]
        except ValueError:
            pass
        i += end_line

    bestfile.write("}")
    bestfile.close()

    return individuals


def search_loop_from_state():
    """
    Run the evolutionary search process from a loaded state. Pick up where
    it left off previously.

    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """
    
    individuals = trackers.state_individuals
        
    # Traditional GE
    for generation in range(stats['gen'] + 1, (params['GENERATIONS'] + 1)):
        stats['gen'] = generation
        
        # New generation
        individuals = params['STEP'](individuals)
            
    return individuals
