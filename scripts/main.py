import sys
import os
import getopt
from Parser import MetricsParser
from Graphs import oquareGraphs

if __name__ == '__main__':

    argv = sys.argv
    outputPath = ""
    inputPath = ""
    plot_models = False
    plot_categories = False
    plot_global = False
    help_msg = "Uso: {0} -i <folderPath> -o <outputPath> -m || -c || -g".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:mcg", ["help", "input=", "output=", "model", "categories", "global"])
    except:
        print(help_msg)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_msg)
            sys.exit(2)
        elif opt in ("-i", "--input"):
            inputPath = arg
        elif opt in ("-o", "--output"):
            outputPath = arg
        elif opt in ("-m", "--model"):
            plot_models = True
        elif opt in ("-c", "--categories"):
            plot_categories = True
        elif opt in ("-g", "--global"):
            plot_global = True

    basepath = inputPath + '/temp_results/'
    oquare_model_values = {}
    graphPlotter = oquareGraphs()
    with os.scandir(basepath) as entries:
        for entry in entries:
            oquare_category_values = {}
            parsed_metrics = MetricsParser(basepath + entry.name + '/metrics/' + entry.name + ".xml")
            categories = parsed_metrics.get_category_metrics()

            if plot_categories:
                for category, values in categories.items():
                    oquare_category_values[category] = values.get('value')
                
                graphPlotter.plot_oquare_categories(oquare_category_values, entry.name)
            
            oquare_model_values[entry.name] = parsed_metrics.get_oquare_value()
    
    if plot_models:
        graphPlotter.plot_oquare_values(oquare_model_values)

    if plot_global:
        archive_path = inputPath + '/archives/'
        oquare_model_values_global = {}
        entries = os.listdir(archive_path)

        # Si hay menos de 18 resultados archivados, los extraigo todos

        if len(entries) < 18:
            # Por cada archivado extraigo las carpetas de ontologias
            for entry in entries:
                with os.scandir(archive_path + entry + '/') as ontologies:
                    for ontology in ontologies:
                        # Si es carpeta (puede haber imagenes de resultados previos)
                        if ontology.is_dir():
                            # Si la entrada no existe para esa ontologia, la añado
                            if not oquare_model_values_global.get(ontology.name):
                                oquare_model_values_global[ontology.name] = list()
                            
                            # Extraigo el oquare_value de esa ontología para ese archivado y la añado a la lista de esa ontologia
                            parsed_metrics = MetricsParser(ontology.path + '/metrics/' + ontology.name + '.xml')
                            oquare_model_values_global.get(ontology.name).append(parsed_metrics.get_oquare_value())
        else:
            for i in range(len(entries)-18, len(entries)):
                entry = entries[i]
                with os.scandir(archive_path + entry + '/') as ontologies:
                    for ontology in ontologies:
                        # Si es carpeta (puede haber imagenes de resultados previos)
                        if ontology.is_dir():
                            # Si la entrada no existe para esa ontologia, la añado
                            if not oquare_model_values_global.get(ontology.name):
                                oquare_model_values_global[ontology.name] = list()
                            
                            # Extraigo el oquare_value de esa ontología para ese archivado y la añado a la lista de esa ontologia
                            parsed_metrics = MetricsParser(ontology.path + '/metrics/' + ontology.name + '.xml')
                            oquare_model_values_global.get(ontology.name).append(parsed_metrics.get_oquare_value())

        # Saco el oquare_value de las ontologias previas a esta ejecución (almacenadas en results)
        results_path = inputPath + '/results/'
        results_entry = os.listdir(results_path)[0]
        with os.scandir(results_path + results_entry) as entries:
            for entry in entries:
                if entry.is_dir():
                    parsed_metrics = MetricsParser(entry.path + '/metrics/' + entry.name + '.xml')
                    oquare_model_values_global.get(entry.name).append(parsed_metrics.get_oquare_value())  

        # Añado el oquare_value que se ha calculado en esta ejecucion
        for ontology in oquare_model_values:
            oquare_model_values_global.get(ontology).append(oquare_model_values.get(ontology))

        # Plot and save
        print(oquare_model_values_global)

