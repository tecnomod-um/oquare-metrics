import sys
import os
import getopt
from Parser import MetricsParser
from Graphs import oquareGraphs
from ReadMeGen import readmeGen
from Controller import Controller

if __name__ == '__main__':

    argv = sys.argv
    inputPath = ""
    plot_models = False
    plot_categories = False
    plot_historic = False
    file = ''
    help_msg = "Uso: {0} -i <folderPath> [-c -f <fileNAME (no extension, no path)>] || [-m -g]".format(argv[0])
    controller = Controller()
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:f:mcg", ["help", "input=", "file=", "model", "categories", "global"])
    except:
        print(help_msg)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_msg)
            sys.exit(2)
        elif opt in ("-i", "--input"):
            inputPath = arg
        elif opt in ("-m", "--model"):
            plot_models = True
        elif opt in ("-c", "--categories"):
            plot_categories = True
        elif opt in ("-g", "--global"):
            plot_historic = True
        elif opt in ("-f", "--file"):
            file = arg

    basepath = inputPath + '/temp_results/'
    graphPlotter = oquareGraphs()
    readmeGenerator = readmeGen()

    if plot_categories:
        if not file or plot_historic or plot_models:
            print(help_msg)
            sys.exit(2)
        
        controller.handle_categories(basepath, file, inputPath)

    else:        
        if plot_models:
            controller.handle_oquare_model(basepath, inputPath)

        if plot_historic:
            controller.handle_historic(basepath, inputPath)

