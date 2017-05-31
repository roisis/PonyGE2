#! /usr/bin/env python

# PonyGE
# Copyright (c) 2009 Erik Hemberg, James McDermott,
#                   Michael Fenton and David Fagan
# Hereby licensed under the GNU GPL v3.
""" Python GE implementation """

from utilities.algorithm.general import check_python_version

check_python_version()

from stats.stats import get_stats
from algorithm.parameters import params, set_params, load_params
from utilities.stats import trackers
import sys


def mane():
    """ Run program """



    # Run evolution
    individuals = params['SEARCH_LOOP']()


    '''
    instruments = ["kick", "hh", "hhOp", "snH", "Sin1", "Sin2"]

    no=1
    #GRAMMAR_FILE = "ChuckGram" + str(no + 1) + ".pybnf"
    resultsFile = open("../results/ChucK/ResultsFile" + str(no) + ".txt", 'w')
    resultsFile.write('Gen \t Ave Fit \t Best Fit \n')

    # Run evolution
    #print(params)
    #params["GRAMMAR_FILE"] = "ChuckGram" + str(no + 1) + ".pybnf"
    individuals = params['SEARCH_LOOP']() #added no i/p by Roisin

    # Print final review
    get_stats(individuals, end=True)


    # Read grammar
    bnf_grammar = Grammar(GRAMMAR_FILE)

    # Create Individuals
    individuals = initialise_population(POPULATION_SIZE)
    # Loop
    best_ever, individuals = search_loop(GENERATIONS, individuals, bnf_grammar,
                                         generational_replacement, tournament_selection,
                                         FITNESS_FUNCTION, resultsFile)

    #for i in individuals:
    #    print(i)


    ind = individuals[0].phenotype
    length = len(ind)

    print("ind: ", ind)
    i = 0
    # Wrie best to file and play with midi
    bestfile = open("../results/ChucK/" + instruments[no] + ".ck", 'w')
    """ Separate individaul into lines and add to file"""
    while i < length:
        # print i
        try:
            end_line = ind.index(";")
            # print "ind: %s end: %d, i: %d"%(ind, end_line, i)
            line = ind[: end_line + 1]
            print("line: ", line)

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

'''

    # Print final review
    get_stats(individuals, end=True)

    # Returns only needed if running experiment manager
    return params['TIME_STAMP'], trackers.best_ever.fitness


if __name__ == "__main__":

    set_params(sys.argv[1:])  # exclude the ponyge.py arg itself
    mane()
