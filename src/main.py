import sys
import getopt
from Controller import Controller

if __name__ == '__main__':

    argv = sys.argv
    input_path = ""
    plot_models = False
    plot_categories = False
    plot_subcategories = False
    plot_metrics = False
    plot_evolution = False
    file = ''
    ontology_source = ''
    date= ""


    controller = Controller()

    try:
        opts, args = getopt.getopt(argv[1:], "i:s:f:McmSed:", ["input=","source=", "file=", "model", "categories", "subcategories", "metrics", "evolution", "date="])
    except:
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_path = arg
        elif opt in ("-s", "--source"):
            ontology_source = arg
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-M", "--model"):  
            plot_models = True
        elif opt in ("-c", "--categories"):
            plot_categories = True
        elif opt in ("-S", "--subcategories"):
            plot_subcategories = True
        elif opt in ("-m", "--metrics"):
            plot_metrics = True
        elif opt in ("-e", "--evolution"):
            plot_evolution = True
        elif opt in ("-d", "--date"):
            date = arg

    temp_path = input_path + '/temp_results/'

    if plot_categories:
        temp_path += ontology_source + '/' + file + '/' + date 
        controller.handle_categories(temp_path, file)

        if plot_evolution:
            controller.handle_category_evolution(file, input_path, ontology_source, date)

    elif plot_subcategories:
        temp_path += ontology_source + '/' + file + '/' + date
        controller.handle_subcategories(temp_path, file)

        if plot_evolution:
            controller.handle_subcategory_evolution(file, input_path, ontology_source, date)
        
    elif plot_models:
        controller.handle_oquare_model(file, input_path, ontology_source, date)

    elif plot_metrics:
        temp_path += ontology_source + '/' + file + '/' + date 
        controller.handle_metrics(temp_path, file)
        if plot_evolution:
            controller.handle_metrics_evolution(file, input_path, ontology_source, date)
        

