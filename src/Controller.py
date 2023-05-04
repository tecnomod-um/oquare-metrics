
import glob
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
    
    def store_characteristics_evolution(self, characteristics: dict, data_store: dict, date: str) -> None:
        """Stores values of characteristics at a certain date in a dictionary
        
        Keyword arguments:
        characteristics -- Dictionary which contains characteristics information such as value
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the characteristics values are associated to

        """
        for characteristic, values in characteristics.items():
            if not data_store.get(characteristic):
                data_store[characteristic] = {}
            
            data_store.get(characteristic)[date] = values.get('value')
    
    def store_subcharacteristics_evolution(self, characteristics: dict, data_store: dict, date: str) -> None:
        """Stores values of subcharacteristics at a certain date in a dictionary
        
        Keyword arguments:
        characteristics -- Dictionary which contains characteristics information such as subcharacteristics values
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the characteristics values are associated to

        """
        for characteristic, values in characteristics.items():
            if not data_store.get(characteristic):
                data_store[characteristic] = {}

            subcharacteristics = values.get('subcharacteristics')

            for subcharacteristic, value in subcharacteristics.items():
                if not data_store.get(characteristic).get(subcharacteristic):
                    data_store.get(characteristic)[subcharacteristic] = {}

                data_store.get(characteristic).get(subcharacteristic)[date] = value        

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
        elif parse_type == 'metrics-scaled':
            scaled_metrics = parsed_metrics.parse_scaled_metrics()
            self.store_metrics_evolution(scaled_metrics, data_store, entry_date)
        elif parse_type == 'characteristics':
            characteristics = parsed_metrics.parse_characteristics_metrics()
            self.store_characteristics_evolution(characteristics, data_store, entry_date)
        elif parse_type == 'subcharacteristics':
            characteristics = parsed_metrics.parse_characteristics_metrics()
            self.store_subcharacteristics_evolution(characteristics, data_store, entry_date)

    def handle_characteristics(self, temp_path: str, file: str) -> None:
        """Handles characteristics data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        oquare_characteristics_values = {}

        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        characteristics = parsed_metrics.parse_characteristics_metrics()
        for characteristic, values in characteristics.items():
            oquare_characteristics_values[characteristic] = values.get('value')
        
        self.graphPlotter.plot_oquare_characteristics(oquare_characteristics_values, file, temp_path)
        self.readmeGenerator.append_characteristics(file, temp_path)

    def handle_subcharacteristics(self, temp_path: str, file: str) -> None:
        """Handles subcharacteristics data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        characteristics = parsed_metrics.parse_characteristics_metrics()
        self.graphPlotter.plot_oquare_subcharacteristics(characteristics, file, temp_path)
        self.readmeGenerator.append_subcharacteristics(file, temp_path, list(characteristics.keys()))


    def handle_metrics(self, temp_path: str, file: str) -> None:
        """Handles metrics data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        metrics = parsed_metrics.parse_metrics()
        scaled_metrics = parsed_metrics.parse_scaled_metrics()

        self.graphPlotter.plot_metrics(metrics, file, temp_path, False)
        self.graphPlotter.plot_metrics(scaled_metrics, file, temp_path, True)
        self.readmeGenerator.append_metrics(file, temp_path)
     
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


        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, oquare_model_values, 'oquare_value') 

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, oquare_model_values, 'oquare_value')

        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        oquare_model_values[date] = parsed_metrics.parse_oquare_value()

        self.graphPlotter.plot_oquare_values(oquare_model_values, file, temp_path)
        self.readmeGenerator.append_oquare_value(file, temp_path)


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
        metrics_evolution_scaled = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, metrics_evolution, 'metrics')
            self.parse_entry(archive_path, path, metrics_evolution_scaled, 'metrics-scaled')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, metrics_evolution, 'metrics')
            self.parse_entry(results_path, results_file_path, metrics_evolution_scaled, 'metrics-scaled')

        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        metrics = parsed_metrics.parse_metrics()
        scaled_metrics = parsed_metrics.parse_scaled_metrics()
        self.store_metrics_evolution(metrics, metrics_evolution, date)
        self.store_metrics_evolution(scaled_metrics, metrics_evolution_scaled, date)
            
        self.graphPlotter.plot_metrics_evolution(metrics_evolution, file, temp_path)
        self.graphPlotter.plot_scaled_metrics_evolution(metrics_evolution_scaled, file, temp_path)
        self.readmeGenerator.append_scaled_metrics_evolution(file, temp_path)
        self.readmeGenerator.append_metrics_evolution(file, temp_path, list(metrics_evolution.keys()))

    def handle_characteristics_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles characteristics evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution
        
        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        characteristics_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, characteristics_evolution, 'characteristics')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, characteristics_evolution, 'characteristics')
                
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        characteristics = parsed_metrics.parse_characteristics_metrics()
        self.store_characteristics_evolution(characteristics, characteristics_evolution, date)

        self.graphPlotter.plot_oquare_characteristics_evolution(characteristics_evolution, file, temp_path)
        self.readmeGenerator.append_characteristics_evolution(file, temp_path)


    def handle_subcharacteristics_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles subcharacteristics evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution
        
        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        subcharacteristics_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, subcharacteristics_evolution, 'subcharacteristics')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, subcharacteristics_evolution, 'subcharacteristics')
                
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        characteristics = parsed_metrics.parse_characteristics_metrics()
        self.store_subcharacteristics_evolution(characteristics, subcharacteristics_evolution, date)

        self.graphPlotter.plot_oquare_subcharacteristics_evolution(subcharacteristics_evolution, file, temp_path)
        self.readmeGenerator.append_subcharacteristics_evolution(file, temp_path, list(characteristics.keys()))
            