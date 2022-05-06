import sys
import getopt
from Controller import Controller

if __name__ == '__main__':

    argv = sys.argv
    input_path = ""
    plot_models = False
    plot_categories = False
    plot_historic = False
    plot_categories_evolution = False
    file = ''
    ontology_source = ''
    code = "0"
    help_msg = "Uso: {0} -i <folderPath> [-c -f <fileNAME (no extension, no path)>] || [-m -g]".format(argv[0])

    controller = Controller()

    try:
        opts, args = getopt.getopt(argv[1:], "hi:s:f:mcgeq:", ["help", "input=","source=", "file=", "model", "categories", "global", "cat_evolution", "code="])
    except:
        print(help_msg)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_msg)
            sys.exit(2)
        elif opt in ("-i", "--input"):
            input_path = arg
        elif opt in ("-m", "--model"):  
            plot_models = True
        elif opt in ("-c", "--categories"):
            plot_categories = True
        elif opt in ("-g", "--global"):
            plot_historic = True
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-s", "--source"):
            ontology_source = arg
        elif opt in ("-e", "--cat_evolution"):
            plot_categories_evolution = True
        elif opt in ("-q", "--code"):
            code = arg

    temp_path = input_path + '/temp_results/'

    if code != "0":
        print('Error: ' + code + ", aborted. Check OQuaRE logs")
        sys.exit()

    if plot_categories:
        if not file or plot_historic or plot_models:
            print(help_msg)
            sys.exit(2)
        
        temp_path += ontology_source + '/'
        controller.handle_categories(temp_path, file, input_path)

    elif plot_categories_evolution:
        controller.handle_category_evolution(file, input_path)
    else:        
        if plot_models:
            controller.handle_oquare_model(temp_path, input_path)

        if plot_historic:
            controller.handle_historic(input_path)

