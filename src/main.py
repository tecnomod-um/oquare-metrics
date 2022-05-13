import sys
import getopt
from Controller import Controller

if __name__ == '__main__':

    argv = sys.argv
    input_path = ""
    plot_models = False
    plot_categories = False
    plot_evolution = False
    plot_metrics = False
    file = ''
    ontology_source = ''
    code = "0"
    date= ""


    controller = Controller()

    try:
        opts, args = getopt.getopt(argv[1:], "i:s:f:Mcemq:d:", ["input=","source=", "file=", "model", "categories", "evolution", "metrics", "code=", "date="])
    except:
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_path = arg
        elif opt in ("-M", "--model"):  
            plot_models = True
        elif opt in ("-c", "--categories"):
            plot_categories = True
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-s", "--source"):
            ontology_source = arg
        elif opt in ("-e", "--evolution"):
            plot_evolution = True
        elif opt in ("-m", "--metrics"):
            plot_metrics = True
        elif opt in ("-q", "--code"):
            code = arg
        elif opt in ("-d", "--date"):
            date = arg

    temp_path = input_path + '/temp_results/'

    if code != "0":
        print('Error: ' + code + ", aborted. Check OQuaRE logs")
        sys.exit()

    if plot_categories:
        temp_path += ontology_source + '/' + file + '/' + date 
        controller.handle_categories(temp_path, file)

    elif plot_evolution:
        controller.handle_category_evolution(file, input_path, ontology_source, date)
        controller.handle_metrics_evolution(file, input_path, ontology_source, date)
    elif plot_models:
        controller.handle_oquare_model(file, input_path, ontology_source, date)
    elif plot_metrics:
        temp_path += ontology_source + '/' + file + '/' + date 
        controller.handle_metrics(temp_path, file)
        

