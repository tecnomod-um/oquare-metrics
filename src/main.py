import sys
import getopt
from Controller import Controller

if __name__ == '__main__':

    argv = sys.argv
    input_path = ""
    plot_models = ''
    plot_characteristics = ''
    plot_subcharacteristics = ''
    plot_metrics = ''
    plot_evolution = ''
    file = ''
    ontology_source = ''
    date= ""


    controller = Controller()

    try:
        opts, args = getopt.getopt(argv[1:], "i:s:f:M:c:S:m:e:d:", 
            ["input=","source=", "file=", "model=", "characteristics=", "subcharacteristics=", "metrics=", "evolution=", "date="])
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
            plot_models = arg
        elif opt in ("-c", "--characteristics"):
            plot_characteristics = arg
        elif opt in ("-S", "--subcharacteristics"):
            plot_subcharacteristics = arg
        elif opt in ("-m", "--metrics"):
            plot_metrics = arg
        elif opt in ("-e", "--evolution"):
            plot_evolution = arg
        elif opt in ("-d", "--date"):
            date = arg

    temp_path = input_path + '/temp_results/'

    if plot_models.lower() == 'true':
        print(temp_path, file, input_path, ontology_source, date)
        controller.handle_oquare_model(file, input_path, ontology_source, date)

    temp_path += ontology_source + '/' + file + '/' + date 

    if plot_characteristics.lower() == 'true':
        controller.handle_characteristics(temp_path, file)
        if plot_evolution.lower() == 'true':
            controller.handle_characteristics_evolution(file, input_path, ontology_source, date)

    if plot_subcharacteristics.lower() == 'true':
        controller.handle_subcharacteristics(temp_path, file)
        if plot_evolution.lower() == 'true':
            controller.handle_subcharacteristics_evolution(file, input_path, ontology_source, date)
        

    if plot_metrics.lower() == 'true':
        controller.handle_metrics(temp_path, file)
        if plot_evolution.lower() == 'true':
            controller.handle_metrics_evolution(file, input_path, ontology_source, date)
        

