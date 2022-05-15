
import glob
from pprint import pprint
import sys
from unicodedata import category
from tools.Plotter import oquareGraphs
from tools.Parser import MetricsParser
from tools.Reporter import readmeGen

class Controller:
    """Controller class that handles file system and additional tool calls

    This class is designed with file system managing responsability in mind, as well
    as calling additional tooling for different purposes. Its responsability lies in
    extracting the paths to metric files aswell as storing and managing extracted data.

    This class makes uses of functionality provided by Plotter, Parser and Reporter classes
    so that it can extract data from metrics files, plot them on different ways and finally
    generate a report which shows different metrics in a visual way.

    """

    def __init__(self):
        """ Controller init method

        Class has a plotter and reporter instances as fields for easy usage

        """
        self.graphPlotter = oquareGraphs()
        self.readmeGenerator = readmeGen()

    def store_metrics_evolution(self, metrics: dict, data_store: dict, date: str) -> None:
        """Stores values of metrics at a certain date in a dictionary
        
        Keyword arguments:
        metrics -- Dictionary which contains all 19 metrics and their values
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the metrics values are associated to

        """
        for metric, value in metrics.items():
            if not data_store.get(metric):
                data_store[metric] = {}
            data_store.get(metric)[date] = value
    
    def store_categories_evolution(self, categories: dict, data_store: dict, date: str) -> None:
        """Stores values of categories at a certain date in a dictionary
        
        Keyword arguments:
        categories -- Dictionary which contains categories information such as value
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the categories values are associated to

        """
        for category, values in categories.items():
            if not data_store.get(category):
                data_store[category] = {}
            
            data_store.get(category)[date] = values.get('value')
    
    def store_subcategories_evolution(self, categories: dict, data_store: dict, date: str) -> None:
        """Stores values of subcategories at a certain date in a dictionary
        
        Keyword arguments:
        categories -- Dictionary which contains categories information such as subcategories values
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the categories values are associated to

        """
        for category, values in categories.items():
            if not data_store.get(category):
                data_store[category] = {}

            subcategories = values.get('subcategories')

            for subcategory, value in subcategories.items():
                if not data_store.get(category).get(subcategory):
                    data_store.get(category)[subcategory] = {}

                data_store.get(category).get(subcategory)[date] = value        

    def parse_entry(self, base_path: str, file_path: str, data_store: dict, parse_type: str) -> None:
        """Parses a file entry to extract its date and store the values on a dict by dates
        
        Keyword arguments:
        base_path -- Path that contains date entries for a given ontology
        file_path -- Full path to an ontology metrics file
        data_store -- Dictionary to store the values for a given date
        parse_type -- Indicates which data should be extracted from metrics and its handling

        """
        entry = file_path.rsplit(base_path, 1)[1]
        entry_date = entry.rsplit('/')[0]
        parsed_metrics = MetricsParser(file_path)

        if parse_type == 'oquare_value':
            data_store[entry_date] = parsed_metrics.parse_oquare_value()
        elif parse_type == 'metrics':
            metrics = parsed_metrics.parse_metrics()
            self.store_metrics_evolution(metrics, data_store, entry_date)
        elif parse_type == 'categories':
            categories = parsed_metrics.parse_category_metrics()
            self.store_categories_evolution(categories, data_store, entry_date)
        elif parse_type == 'subcategories':
            categories = parsed_metrics.parse_category_metrics()
            self.store_subcategories_evolution(categories, data_store, entry_date)

    def handle_categories(self, temp_path: str, file: str) -> None:
        """Handles category data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        oquare_category_values = {}

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            categories = parsed_metrics.parse_category_metrics()
            for category, values in categories.items():
                oquare_category_values[category] = values.get('value')
            
            self.graphPlotter.plot_oquare_categories(oquare_category_values, file, temp_path)
            self.readmeGenerator.append_category(file, temp_path)

        except FileNotFoundError as e:
            print("Error CATEGORY PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()

    def handle_subcategories(self, temp_path: str, file: str) -> None:
        """Handles subcategory data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            categories = parsed_metrics.parse_category_metrics()
            self.graphPlotter.plot_oquare_subcategories(categories, file, temp_path)
            self.readmeGenerator.append_subcategory(file, temp_path, list(categories.keys()))

        except FileNotFoundError as e:
            print("Error SUBCATEGORY PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()

    def handle_metrics(self, temp_path: str, file: str) -> None:
        """Handles metrics data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            metrics = parsed_metrics.parse_metrics()
            scaled_metrics = parsed_metrics.parse_scaled_metrics()

            self.graphPlotter.plot_metrics(metrics, file, temp_path, False)
            self.graphPlotter.plot_metrics(scaled_metrics, file, temp_path, True)
            self.readmeGenerator.append_metrics(file, temp_path)

        except FileNotFoundError as e:
            print("Error METRICS: " + e.strerror + ". Abort", flush=True)
     
    def handle_oquare_model(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles oquare model evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution

        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        oquare_model_values = {}


        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            self.parse_entry(archive_path, path, oquare_model_values, 'oquare_value') 

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, oquare_model_values, 'oquare_value')

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            oquare_model_values[date] = parsed_metrics.parse_oquare_value()

            self.graphPlotter.plot_oquare_values(oquare_model_values, temp_path)
            self.readmeGenerator.append_oquare_value(temp_path)
            
        except FileNotFoundError as e:
            print("Error MODEL PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()    

    def handle_metrics_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles metrics evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution

        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        metrics_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            self.parse_entry(archive_path, path, metrics_evolution, 'metrics')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, metrics_evolution, 'metrics')

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            metrics = parsed_metrics.parse_metrics()
            self.store_metrics_evolution(metrics, metrics_evolution, date)
                
            self.graphPlotter.plot_metrics_evolution(metrics_evolution, temp_path)
            self.readmeGenerator.append_metrics_evolution(temp_path, list(metrics_evolution.keys()))
        except FileNotFoundError as e:
            print("Error METRICS EVOLUTION: " + e.strerror + ". Abort", flush=True)
            sys.exit()  

    def handle_category_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles category evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution
        
        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        categories_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            self.parse_entry(archive_path, path, categories_evolution, 'categories')

        results_file_path = glob.glob(results_path + ontology_source + '/' + file + '/*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, categories_evolution, 'categories')
                
        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            categories = parsed_metrics.parse_category_metrics()
            self.store_categories_evolution(categories, categories_evolution, date)

            self.graphPlotter.plot_oquare_category_evolution(categories_evolution, temp_path)
            self.readmeGenerator.append_category_evolution(temp_path)
            
        except FileNotFoundError as e:
            print("Error CATEGORY EVOLUTION PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()

    def handle_subcategory_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles subcategory evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution
        
        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        subcategories_evolution = {}

        """
            
        categoria: {
            subcat1: {
                fecha1: valor,
                fecha2: valor,
                fecha3: valor
            },
            subcat2: {
                fecha1: valor,
                fecha2: valor,
                fecha3: valor
            }
        }
        
        """

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            print(path)
            self.parse_entry(archive_path, path, subcategories_evolution, 'subcategories')

        results_file_path = glob.glob(results_path + ontology_source + '/' + file + '/*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, subcategories_evolution, 'subcategories')
                
        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            categories = parsed_metrics.parse_category_metrics()
            self.store_subcategories_evolution(categories, subcategories_evolution, date)

            #pprint(subcategories_evolution)

            #self.graphPlotter.plot_oquare_category_evolution(categories_evolution, temp_path)
            #self.readmeGenerator.append_category_evolution(temp_path)
            
        except FileNotFoundError as e:
            print("Error SUBCATEGORY EVOLUTION PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()