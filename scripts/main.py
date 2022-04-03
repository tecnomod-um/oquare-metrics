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
    help_msg = "Uso: {0} -i <folderPath> -o <outputPath> -m || -c".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:mc", ["help", "input=", "output=", "model", "categories"])
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
    
    if plot_models and plot_categories:
        print(help_msg)
        sys.exit(2)
    
    if plot_models:
        basepath = inputPath + '/temp_results/'
        oquare_model_values = {}
        with os.scandir(basepath) as entries:
            for entry in entries:
                parsed_metrics = MetricsParser(basepath + entry.name + '/metrics/' + entry.name + ".xml")
                oquare_model_values[entry.name] = parsed_metrics.get_oquare_value()
        
        graphPlotter = oquareGraphs()
        graphPlotter.plot_oquare_values(oquare_model_values, outputPath)
        sys.exit(0)
    
    if plot_categories:
        sys.exit(0) 


    # Tras la ejecución de oquare, tengo todos los ficheros .xml almacenados en ./temp_results/{nombre_ontologia}/metrics/
    # Por lo tanto en temp_results tengo una carpeta por ontologia --> Recorro carpeta temp_results
    # Por cada carpeta de temp_results, navego a ./temp_results/{carpeta}/metrics/{carpeta}.xml y hago un MetricsParser 
    # Una vez obtenido todos los MetricsParser, llamo a oquareGraphs con el array de MetricsParser
    # Por último, oquareGraphs se encarga de hacer un plot de cada uno de los oquareValues. Necesario guardar el nombre de la ontología en algun sitio.