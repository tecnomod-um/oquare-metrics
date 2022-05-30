import sys
import getopt
from Controller import Controller

if __name__ == '__main__':

    argv = sys.argv
    input_path = ""
    plot_models = ''
    plot_features = ''
    plot_subfeatures = ''
    plot_metrics = ''
    plot_evolution = ''
    file = ''
    ontology_source = ''
    date= ""


    controller = Controller()

    try:
        opts, args = getopt.getopt(argv[1:], "i:s:f:M:c:S:m:e:d:", 
            ["input=","source=", "file=", "model=", "features=", "subfeatures=", "metrics=", "evolution=", "date="])
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
        elif opt in ("-c", "--features"):
            plot_features = arg
        elif opt in ("-S", "--subfeatures"):
            plot_subfeatures = arg
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

    if plot_features.lower() == 'true':
        controller.handle_features(temp_path, file)
        if plot_evolution.lower() == 'true':
            controller.handle_features_evolution(file, input_path, ontology_source, date)

    if plot_subfeatures.lower() == 'true':
        controller.handle_subfeatures(temp_path, file)
        if plot_evolution.lower() == 'true':
            controller.handle_subfeatures_evolution(file, input_path, ontology_source, date)
        

    if plot_metrics.lower() == 'true':
        controller.handle_metrics(temp_path, file)
        if plot_evolution.lower() == 'true':
            controller.handle_metrics_evolution(file, input_path, ontology_source, date)
        

