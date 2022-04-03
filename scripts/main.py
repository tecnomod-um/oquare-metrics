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
        opts, args = getopt.getopt(argv[1:], "hi:o:mc", ["help", "input=", "output=", "model", "categories", "global"])
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


                


    # Tras la ejecución de oquare, tengo todos los ficheros .xml almacenados en ./temp_results/{nombre_ontologia}/metrics/
    # Por lo tanto en temp_results tengo una carpeta por ontologia --> Recorro carpeta temp_results
    # Por cada carpeta de temp_results, navego a ./temp_results/{carpeta}/metrics/{carpeta}.xml y hago un MetricsParser 
    # Una vez obtenido todos los MetricsParser, llamo a oquareGraphs con el array de MetricsParser
    # Por último, oquareGraphs se encarga de hacer un plot de cada uno de los oquareValues. Necesario guardar el nombre de la ontología en algun sitio.


    # En cada ejecución de OQuaRE, cuando termina de ejecutarse es cuando puedo hacer una gráfica de los resultados de las categorias.
    # O se puede ejecutar todo al final y simplemente indicar una serie de flags para saber que gráficas se dibujan.

    # Para las categorias, por cada "entry" de entries en el bucle dentro de plot_model, se obtendrian el dict con las categorias y se saca value.
    # Con eso se hace el plotting.

    # Por ultimo si se quiere hacer una grafica global que tenga en cuenta el historico, se ha de recorrer la carpeta archives.
    # Se puede utilizar los ultimos 19 archivados + el reciente para obtener los datos. Una sola gráfica de líneas. Cada línea representa una ontología
    # Los valores que se utilizan son los de oquareModel (get_oquare_value)